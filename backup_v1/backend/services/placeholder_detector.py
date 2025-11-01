"""
Placeholder Detector Service
=============================
Intelligently identifies and extracts placeholders from legal documents
using multiple detection strategies including regex patterns, contextual
analysis, and legal terminology understanding.

This module provides:
- Multiple pattern detection ({{}}, [], __, <> formats)
- Contextual placeholder identification
- Type inference based on placeholder names
- Grouping of related placeholders
- Value suggestions based on context

Author: Legal Tech Solutions
Date: October 2025
Version: 1.0.0
"""

import re
import logging
from typing import List, Dict, Any, Optional, Set, Tuple
from collections import OrderedDict
from datetime import datetime, timedelta
from uuid import uuid4

# Configure logging
logger = logging.getLogger(__name__)


class PlaceholderDetector:
    """
    Intelligent placeholder detection for legal documents.
    
    This detector:
    - Identifies placeholders in various formats
    - Infers placeholder types from context
    - Groups related fields together
    - Provides smart value suggestions
    """
    
    def __init__(self):
        """
        Initialize the PlaceholderDetector with patterns and keywords.
        """
        # Define placeholder patterns to search for
        self.patterns = [
            # $[__________] style - MUST come first for dollar amounts
            (r'\$\[([^\]]*)\]', 'dollar_bracket'),
            # [ANY TEXT] style - case insensitive, matches any text in brackets
            (r'\[([^\]]+)\]', 'square_bracket'),
            # {{placeholder}} style - common
            (r'\{\{([^}]+)\}\}', 'double_curly'),
            # __PLACEHOLDER__ style (with actual text, not just underscores)
            (r'__([A-Za-z][A-Za-z_\s]*[A-Za-z])__', 'underscore'),
            # <PLACEHOLDER> style
            (r'<([A-Z_\s]+)>', 'angle_bracket'),
            # [INSERT PLACEHOLDER] style
            (r'\[INSERT ([^]]+)\]', 'insert_style'),
            # _______ (Name) style - blanks with description
            (r'_{3,}\s*\(([^)]+)\)', 'blank_with_description'),
            # Field: _______ style
            (r'([A-Za-z\s]+):\s*_{3,}', 'field_with_blank'),
        ]
        
        # Common legal placeholder keywords
        self.legal_keywords = [
            'Company Name', 'Investor Name', 'Date', 'Amount',
            'Valuation Cap', 'Discount Rate', 'Address', 'State of Incorporation',
            'Email', 'Phone', 'Signature', 'Title', 'Jurisdiction',
            'Effective Date', 'Termination Date', 'Purchase Price',
            'Number of Shares', 'Interest Rate', 'Payment Terms',
            'Governing Law', 'Notice Address', 'Tax ID', 'Registration Number'
        ]
        
        # Field type indicators for intelligent detection
        self.type_indicators = {
            'company': ['company', 'corporation', 'entity', 'business', 'firm', 'organization', 'llc', 'inc', 'corp'],
            'person': ['name', 'person', 'individual', 'party', 'signatory', 'representative', 'employee'],
            'date': ['date', 'day', 'month', 'year', 'effective', 'expiration', 'deadline', 'due', 'termination'],
            'amount': ['amount', 'price', 'fee', 'cost', 'payment', 'sum', 'total', 'valuation', 'cap', '$', 'dollar', 'usd'],
            'percentage': ['percentage', 'percent', 'rate', 'discount', 'interest', 'commission', '%'],
            'address': ['address', 'location', 'street', 'city', 'state', 'zip', 'country', 'jurisdiction'],
            'contact': ['email', 'phone', 'telephone', 'fax', 'contact', 'mobile', 'tel'],
            'number': ['number', 'count', 'quantity', 'shares', 'units', '#', 'no.'],
            'signature': ['signature', 'signed', 'authorized', 'executed', 'acknowledged'],
            'title': ['title', 'position', 'role', 'designation', 'office']
        }
        
        logger.info("PlaceholderDetector initialized with %d patterns", len(self.patterns))
    
    def detect_placeholders(self, document_content: Dict[str, Any]) -> List[Dict]:
        """
        Detect all placeholders in the document.
        
        This method:
        1. Searches for pattern-based placeholders
        2. Identifies contextual placeholders
        3. Removes duplicates while preserving order
        4. Sorts by appearance order
        
        Args:
            document_content (Dict): Parsed document content
            
        Returns:
            List[Dict]: List of unique placeholders with metadata
        """
        all_placeholders = []  # Collect ALL placeholders first (no deduplication yet)
        
        # Search in paragraphs
        for para_data in document_content.get('paragraphs', []):
            text = para_data['text']
            found = self._find_placeholders_in_text(
                text=text,
                location=para_data['index'],
                location_type='paragraph'
            )
            
            for placeholder in found:
                all_placeholders.append(placeholder)
                logger.debug(f"Found placeholder in paragraph: {placeholder['name']}")
        
        # Search in tables
        for table_data in document_content.get('tables', []):
            for row_idx, row in enumerate(table_data['rows']):
                for col_idx, cell in enumerate(row):
                    # Handle both dict and string cell formats
                    cell_text = cell['text'] if isinstance(cell, dict) else str(cell)
                    
                    found = self._find_placeholders_in_text(
                        text=cell_text,
                        location=f"{table_data['index']}-{row_idx}-{col_idx}",
                        location_type='table'
                    )
                    
                    for placeholder in found:
                        all_placeholders.append(placeholder)
                        logger.debug(f"Found placeholder in table: {placeholder['name']}")
        
        # Check for contextual placeholders (blanks that should be filled)
        # NOTE: Disabled to avoid creating non-fillable placeholders
        # contextual = self._detect_contextual_placeholders(document_content)
        # for placeholder in contextual:
        #     key = placeholder['key']
        #     if key not in seen_placeholders:
        #         seen_placeholders[key] = placeholder
        #         logger.debug(f"Found contextual placeholder: {placeholder['name']}")
        
        # Smart deduplication based on context (not just normalized key)
        placeholders = self._smart_deduplicate(all_placeholders)
        
        # Sort by location AND position (appearance order in document)
        placeholders.sort(key=lambda x: (
            x['location_type'],
            x['location'] if isinstance(x['location'], int) else str(x['location']),
            x['position'][0]  # Character position within paragraph
        ))
        
        # Filter out problematic placeholders
        filtered_placeholders = self._filter_placeholders(placeholders, document_content)
        
        # Add sequence numbers for better tracking
        for i, placeholder in enumerate(filtered_placeholders):
            placeholder['sequence'] = i + 1
        
        logger.info(f"Detected {len(placeholders)} placeholders, {len(filtered_placeholders)} after filtering")
        return filtered_placeholders
    
    def _find_placeholders_in_text(self, text: str, location: Any,
                                  location_type: str) -> List[Dict]:
        """
        Find placeholders in a given text using various patterns.
        
        Args:
            text (str): Text to search
            location (Any): Location identifier
            location_type (str): Type of location (paragraph/table)
            
        Returns:
            List[Dict]: Found placeholders with metadata
        """
        found_placeholders = []
        
        # Try each pattern
        for pattern, pattern_type in self.patterns:
            try:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                
                for match in matches:
                    full_match = match.group(0)
                    
                    # Extract the placeholder text based on pattern type
                    if pattern_type == 'dollar_bracket':
                        # For $[____] or $[text], infer from context
                        context = self._extract_context(text, match.span(), 200)  # Expanded context for better detection
                        captured_text = match.group(1).strip() if match.groups() else ''
                        if captured_text and captured_text != '_' * len(captured_text):
                            # Has actual text inside
                            placeholder_text = captured_text
                        else:
                            # Blank or underscores - infer from context
                            placeholder_text = self._infer_placeholder_name(full_match, context)
                    elif pattern_type == 'field_with_blank':
                        # For "Field: _____" pattern, the field name is in group 1
                        if match.groups():
                            placeholder_text = match.group(1).strip()
                        else:
                            continue
                    else:
                        # Most patterns capture the placeholder name in group 1
                        if match.groups():
                            placeholder_text = match.group(1).strip()
                        else:
                            # Skip patterns with no capture groups
                            continue
                    
                    # Clean and normalize the placeholder name
                    cleaned_name = self._clean_placeholder_name(placeholder_text)
                    
                    # Skip if empty after cleaning or too short
                    if not cleaned_name or len(cleaned_name) < 2:
                        continue
                    
                    # Skip common words that aren't placeholders
                    if cleaned_name.lower() in ['the', 'this', 'that', 'section', 'see']:
                        continue
                    
                    # Create placeholder data
                    # Generate normalized key for deduplication
                    normalized_key = self._generate_normalized_key(cleaned_name)
                    unique_key = f"{normalized_key}_{location}"
                    occurrence_id = f"ph_{uuid4().hex[:8]}"
                    
                    placeholder_data = {
                        'id': occurrence_id,  # NEW: per-occurrence id
                        'key': unique_key,
                        'normalized_key': normalized_key,  # For deduplication
                        'name': cleaned_name,
                        'original': full_match,
                        'type': self._identify_placeholder_type(cleaned_name),
                        'pattern_type': pattern_type,
                        'location': location,
                        'location_type': location_type,
                        'position': match.span(),
                        'context': self._extract_context(text, match.span()),
                        'required': True,  # Assume all placeholders are required
                        'suggestions': []  # Will be populated later if needed
                    }
                    
                    found_placeholders.append(placeholder_data)
                    
            except Exception as e:
                logger.warning(f"Error with pattern {pattern}: {str(e)}")
                continue
        
        return found_placeholders
    
    def _smart_deduplicate(self, all_placeholders: List[Dict]) -> List[Dict]:
        """
        Smart deduplication that uses CONTEXT to differentiate identical patterns.
        
        Key logic:
        - For identical patterns like $[___], check CONTEXT to determine if they're different fields
        - Example: $[___] with "purchase amount" context vs $[___] with "valuation cap" context
        - CRITICAL: NEVER merge placeholders in different locations - always keep them separate
        - Only merge truly identical fields (same name + same context + SAME location)
        
        Args:
            all_placeholders: All detected placeholders (may have duplicates)
            
        Returns:
            List of unique placeholders with context-aware deduplication
        """
        if not all_placeholders:
            return []
        
        # Group by context-aware signature + location to ensure different locations stay separate
        groups = {}
        
        for p in all_placeholders:
            name_lower = p['name'].lower().strip()
            context_lower = p.get('context', '').lower()
            original = p['original']
            location = p['location']
            location_type = p['location_type']
            
            # Special handling for identical patterns (like $[___] or [___])
            # CRITICAL: Include location in signature to prevent merging across different locations
            if original.startswith('$[') or (original.startswith('[') and len(original) > 10):
                # Check if it's a blank dollar amount pattern (with underscores)
                is_blank_dollar = original.startswith('$[') and ('_' in original or len(original) > 8)
                if is_blank_dollar:
                    # Use CONTEXT to differentiate, but ALWAYS include location
                    if 'purchase amount' in context_lower or 'payment by' in context_lower or 'exchange for' in context_lower:
                        signature = f'purchase_amount_{location_type}_{location}'
                    elif 'post-money valuation cap' in context_lower or 'valuation cap' in context_lower:
                        signature = f'valuation_cap_{location_type}_{location}'
                    elif 'post money' in context_lower:
                        signature = f'valuation_cap_{location_type}_{location}'
                    else:
                        # Fallback: use location to keep them separate
                        signature = f"amount_field_{location_type}_{location}"
                else:
                    # Has actual text inside - use name + location
                    signature = f"{name_lower}_{location_type}_{location}"
            else:
                # For named placeholders, include location to prevent cross-location merging
                normalized_key = p.get('normalized_key', name_lower)
                signature = f"{normalized_key}_{location_type}_{location}"
            
            if signature not in groups:
                groups[signature] = []
            groups[signature].append(p)
        
        # For each group, handle duplicates
        unique = []
        for signature, group in groups.items():
            if len(group) == 1:
                # Single occurrence - keep it
                unique.append(group[0])
            else:
                # Multiple occurrences with same signature - these are true duplicates
                # Sort by position within the same location and keep only the first
                group.sort(key=lambda x: x['position'][0])
                
                # Only deduplicate if they're in the EXACT same location and position is very close
                # (within 10 characters suggests it's the same placeholder detected twice)
                filtered_group = []
                seen_positions = set()
                
                for p in group:
                    pos_key = (p['position'][0], p['position'][1])
                    # Only consider it a duplicate if position is very close (within 10 chars)
                    is_duplicate = False
                    for seen_pos in seen_positions:
                        if abs(pos_key[0] - seen_pos[0]) < 10:
                            is_duplicate = True
                            break
                    
                    if not is_duplicate:
                        filtered_group.append(p)
                        seen_positions.add(pos_key)
                
                # Keep all non-duplicate occurrences
                unique.extend(filtered_group)
                
                if len(group) > len(filtered_group):
                    logger.info(f"Deduplicated {len(group) - len(filtered_group)} duplicate occurrences of '{group[0]['name']}' (signature: {signature})")
        
        logger.info(f"Smart deduplication: {len(all_placeholders)} total → {len(unique)} unique")
        return unique
    
    def _detect_contextual_placeholders(self, content: Dict[str, Any]) -> List[Dict]:
        """
        Detect contextual placeholders that might not follow standard patterns.
        
        This includes:
        - Lines with blanks to fill
        - Form-style fields
        - Implicit placeholders
        - Label-only paragraphs followed by blank paragraphs
        
        Args:
            content (Dict): Document content
            
        Returns:
            List[Dict]: Contextual placeholders found
        """
        contextual_placeholders = []
        
        # Patterns for contextual detection
        blank_patterns = [
            # Field Name: ________
            (r'([A-Za-z\s]+):\s*_{3,}', 'field_blank'),
            # Field Name ________
            (r'([A-Za-z\s]+)\s+_{3,}', 'field_space_blank'),
            # ________ (Field Name)
            (r'_{3,}\s*\(([^)]+)\)', 'blank_description'),
            # By: ________ Name: ________
            (r'([A-Za-z]+):\s*_{3,}', 'label_blank'),
        ]
        
        # Search paragraphs for contextual patterns
        for para_data in content.get('paragraphs', []):
            text = para_data['text']
            
            for pattern, pattern_name in blank_patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                
                for match in matches:
                    # Extract field name
                    if pattern_name in ['blank_description']:
                        field_name = match.group(1).strip()
                    else:
                        field_name = match.group(1).strip()
                    
                    # Clean the field name
                    field_name = self._clean_placeholder_name(field_name)
                    
                    if not field_name or len(field_name) < 2:
                        continue
                    
                    # Create placeholder data
                    placeholder_data = {
                        'key': self._generate_placeholder_key(field_name),
                        'name': field_name,
                        'original': match.group(0),
                        'type': self._identify_placeholder_type(field_name),
                        'pattern_type': f'contextual_{pattern_name}',
                        'location': para_data['index'],
                        'location_type': 'paragraph',
                        'position': match.span(),
                        'context': self._extract_context(text, match.span()),
                        'required': True,
                        'suggestions': []
                    }
                    
                    contextual_placeholders.append(placeholder_data)
        
        # Detect label-only paragraphs followed by blank paragraphs (form-style fields)
        # We need to check the RAW paragraphs, not the filtered ones
        paragraphs = content.get('paragraphs', [])
        
        # Create a map of original indices for gap checking
        para_map = {para_data['index']: para_data for para_data in paragraphs}
        
        for i, para_data in enumerate(paragraphs):
            text = para_data['text'].strip()
            current_idx = para_data['index']
            
            # Check if this is a label-only paragraph (ends with colon, no other content)
            # Pattern: "Field Name:" or "Label:" 
            if re.match(r'^[A-Za-z][A-Za-z\s]+:\s*$', text):
                # Check if the next paragraph is blank or has minimal content
                # Need to check both the list index AND the document index
                is_last = (i + 1 >= len(paragraphs))
                should_consider = False
                
                if is_last:
                    # Last paragraph is always a form field if it's a label
                    should_consider = True
                else:
                    next_para = paragraphs[i + 1]
                    next_idx = next_para['index']
                    next_text = next_para['text'].strip()
                    
                    # Check if there's a gap (empty paragraph) or if next is actually blank
                    # Gap indicates empty paragraph in raw document
                    has_gap = (next_idx - current_idx) > 1
                    
                    # If next paragraph is blank or we have a gap, this is a form field
                    should_consider = (has_gap or not next_text or len(next_text) < 2)
                
                if should_consider:
                    # Skip labels that are already detected as part of previous patterns
                    # (like "By:", "Name:", etc. that might already have placeholders nearby)
                    field_name = re.sub(r':\s*$', '', text).strip()
                    
                    # Skip if already detected or if it's a generic label
                    field_name_clean = self._clean_placeholder_name(field_name)
                    
                    # Skip label-only signature fields (Address:, Email:) as they can't be filled
                    # These don't have actual placeholders to replace in the document
                    is_signature_label = field_name_clean.lower() in ['address', 'email']
                    
                    if is_signature_label:
                        # Skip these - they're just labels without fillable placeholders
                        continue
                    
                    # Use location-based key for contextual placeholders
                    key = self._generate_placeholder_key(field_name_clean, current_idx)
                    
                    if len(field_name_clean) >= 2:
                        # Create placeholder for this blank field
                        placeholder_data = {
                            'key': key,
                            'name': field_name_clean,
                            'original': f"{text} ______",  # Show as "Label: ______"
                            'type': self._identify_placeholder_type(field_name_clean),
                            'pattern_type': 'contextual_form_field',
                            'location': para_data['index'],
                            'location_type': 'paragraph',
                            'position': (0, len(text)),
                            'context': f"{text} [...]",
                            'required': True,
                            'suggestions': []
                        }
                        
                        contextual_placeholders.append(placeholder_data)
        
        return contextual_placeholders
    
    def _clean_placeholder_name(self, name: str) -> str:
        """
        Clean and normalize placeholder name.
        
        Args:
            name (str): Raw placeholder name
            
        Returns:
            str: Cleaned name
        """
        # Remove extra whitespace
        name = ' '.join(name.split())
        
        # Convert to title case if all uppercase
        if name.isupper() and len(name) > 2:
            name = name.title()
        
        # Remove common prefixes that don't add value
        prefixes_to_remove = ['Insert', 'Enter', 'Add', 'Input', 'Type', 'Provide', 'Fill']
        for prefix in prefixes_to_remove:
            if name.startswith(prefix + ' '):
                name = name[len(prefix)+1:]
            elif name.startswith(prefix.upper() + ' '):
                name = name[len(prefix)+1:]
        
        # Handle special cases - only apply if exact word match
        replacements = {
            'Co.': 'Company',
            'Corp.': 'Corporation',
            'Inc.': 'Incorporated',
            'Addr': 'Address',
            'Amt': 'Amount',
            'Pct': 'Percentage',
            'No.': 'Number',
            'Tel': 'Telephone',
            'Qty': 'Quantity'
        }
        
        for old, new in replacements.items():
            # Only replace if it's a full word match
            pattern = r'\b' + re.escape(old) + r'\b'
            name = re.sub(pattern, new, name)
        
        return name.strip()
    
    def _generate_normalized_key(self, name: str) -> str:
        """
        Generate a normalized key for deduplication (without location).
        Maps similar names to the same key.
        
        Args:
            name (str): Placeholder name
            
        Returns:
            str: Normalized key
        """
        # Create a clean key from the name
        key = name.lower().strip()
        
        # Replace spaces and special characters
        key = re.sub(r'[^a-z0-9]+', '_', key)
        
        # Remove leading/trailing underscores
        key = key.strip('_')
        
        # Standardize common variations - keep each unique field separate
        # CRITICAL: purchase_amount and valuation_cap are SEPARATE fields!
        key_mappings = {
            'company_name': 'company_name',
            'company': 'company_name',
            'investor_name': 'investor_name',
            'investor': 'investor_name',
            'purchase_amount': 'purchase_amount',
            'date_of_safe': 'date_of_safe',
            'safe_date': 'date_of_safe',
            'state_of_incorporation': 'state_of_incorporation',
            # Valuation Cap variations - all map to same key
            'valuation_cap': 'valuation_cap',
            'valuation_cap_amount': 'valuation_cap',
            'post_money_valuation_cap': 'valuation_cap',
            'postmoney_valuation_cap': 'valuation_cap',
            'post_money_valuation_cap': 'valuation_cap',
            'governing_law_jurisdiction': 'governing_law_jurisdiction',
            'governing_law': 'governing_law_jurisdiction',
            # Keep 'name' and 'title' as separate fields (signature fields)
            'name': 'signatory_name',
            'title': 'signatory_title',
        }
        
        return key_mappings.get(key, key)
    
    def _generate_placeholder_key(self, name: str, location: Optional[Any] = None) -> str:
        """
        Generate a unique key for the placeholder (deprecated - use normalized_key).
        
        Args:
            name (str): Placeholder name
            location (Optional[Any]): Location context to differentiate duplicates
            
        Returns:
            str: Unique key
        """
        # Create a clean key from the name
        key = name.lower()
        
        # Replace spaces and special characters
        key = re.sub(r'[^a-z0-9]+', '_', key)
        
        # Remove leading/trailing underscores
        key = key.strip('_')
        
        # Ensure it's not empty
        if not key:
            key = 'placeholder'
        
        # Add location suffix for duplicate differentiation
        if location is not None:
            key = f"{key}_{location}"
        
        return key
    
    def _identify_placeholder_type(self, name: str) -> str:
        """
        Identify the type of placeholder based on its name.
        
        Args:
            name (str): Placeholder name
            
        Returns:
            str: Identified type
        """
        name_lower = name.lower()
        
        # CRITICAL: Check special cases FIRST (before type_indicators)
        # to avoid false matches (e.g., "State of Incorporation" should be 'address', not 'company')
        
        # Special cases for compound phrases
        # IMPORTANT: Check address fields FIRST to override 'party' matching in person type
        if 'address' in name_lower:
            return 'address'
        elif 'state of incorporation' in name_lower:
            return 'address'
        elif 'governing law' in name_lower or 'governing law jurisdiction' in name_lower:
            return 'address'
        elif 'valuation cap' in name_lower:
            return 'amount'
        elif 'discount rate' in name_lower:
            return 'percentage'
        elif 'purchase amount' in name_lower:
            return 'amount'
        elif 'date of safe' in name_lower or 'safe date' in name_lower:
            return 'date'
        elif 'investor name' in name_lower:
            return 'person'
        elif 'company name' in name_lower:
            return 'company'
        # Special handling for "Term Months", "Number of Months" etc. - these are numbers, not dates
        elif ('term' in name_lower and 'month' in name_lower) or ('number of month' in name_lower) or ('month' in name_lower and any(word in name_lower for word in ['term', 'number', 'count', 'quantity', 'duration', 'period'])):
            return 'number'
        
        # Check each type's indicators (after special cases)
        for type_name, indicators in self.type_indicators.items():
            if any(indicator in name_lower for indicator in indicators):
                # Additional validation for 'company' type - exclude addresses
                if type_name == 'company' and ('state' in name_lower and 'incorporation' in name_lower):
                    continue  # Skip, this should be address
                return type_name
        
        # Default to text type
        return 'text'
    
    def _extract_context(self, text: str, position: Tuple[int, int],
                        context_size: int = 50) -> str:
        """
        Extract surrounding context for a placeholder.
        
        Args:
            text (str): Full text
            position (Tuple[int, int]): Start and end position
            context_size (int): Characters of context on each side
            
        Returns:
            str: Context string
        """
        start, end = position
        
        # Calculate context boundaries
        context_start = max(0, start - context_size)
        context_end = min(len(text), end + context_size)
        
        # Extract context
        context = text[context_start:context_end]
        
        # Add ellipsis if truncated
        if context_start > 0:
            context = '...' + context
        if context_end < len(text):
            context = context + '...'
        
        return context
    
    def _filter_placeholders(self, placeholders: List[Dict], document_content: Dict) -> List[Dict]:
        """
        Filter out problematic placeholders that shouldn't be prompted.
        
        Args:
            placeholders: List of detected placeholders
            document_content: Parsed document content
            
        Returns:
            List of filtered placeholders
        """
        filtered = []
        
        # Filter out problematic placeholders
        for placeholder in placeholders:
            name = placeholder['name']
            location = placeholder['location']
            
            # Skip empty/blank placeholders (underscores only)
            if not name or name == '_' * len(name):
                logger.debug(f"Skipping blank placeholder at location {location}")
                continue
            
            # NOTE: Removed Valuation Cap filtering - now handled by context-aware deduplication
            # Both Purchase Amount and Valuation Cap are valid separate fields in SAFE documents
            
            filtered.append(placeholder)
        
        return filtered
    
    def _infer_placeholder_name(self, placeholder_match: str, context: str) -> str:
        """
        Infer a placeholder name from context when the placeholder itself is just blanks.
        
        IMPROVED: Better detection of Purchase Amount vs Valuation Cap
        
        Args:
            placeholder_match (str): The matched placeholder (e.g., "_____" or "$[____]")
            context (str): Surrounding text
            
        Returns:
            str: Inferred placeholder name
        """
        # CRITICAL: Check context for specific keywords FIRST (expanded context window)
        context_lower = context.lower()
        
        # Check for Valuation Cap indicators FIRST (more specific)
        if 'post-money valuation cap' in context_lower or 'post money valuation cap' in context_lower or 'valuation cap' in context_lower:
            return 'Post-Money Valuation Cap'
        
        if 'post money' in context_lower:
            return 'Post-Money Valuation Cap'
        
        # Check for Purchase Amount indicators
        if 'purchase amount' in context_lower or 'payment by' in context_lower or 'exchange for' in context_lower:
            return 'Purchase Amount'
        
        # Look for common patterns before the placeholder
        patterns = [
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+is\s*$',  # "Purchase Amount is"
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*[:\-]\s*$',  # "Company Name: _____"
            r'[Bb]y\s+([A-Za-z\s]+?)[:]\s*$',  # "by Investor Name:" or "By: _____"
            r'^([A-Za-z\s]+):\s*$',  # "Name:" at start
            r'([A-Z][A-Za-z\s]{3,30})\s+(?:of|for)\s*$',  # "State of Incorporation"
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*\($',  # "Name ("
        ]
        
        # Try to extract field name from context before placeholder
        before_text = context.split(placeholder_match)[0] if placeholder_match in context else context
        before_text = before_text[-100:].strip()  # Increased to 100 chars for better context
        
        # Try patterns in order
        for pattern in patterns:
            match = re.search(pattern, before_text, re.IGNORECASE)
            if match:
                inferred = match.group(1).strip()
                # Clean up common prefixes
                inferred = re.sub(r'^(the|a|an)\s+', '', inferred, flags=re.IGNORECASE)
                # Capitalize properly
                inferred = ' '.join(word.capitalize() for word in inferred.split())
                # Validate it's not too short or common
                if len(inferred) >= 3 and inferred.lower() not in ['the', 'and', 'for', 'with', 'this', 'that']:
                    return inferred
        
        # Check text after placeholder for hints
        after_text = context.split(placeholder_match)[1] if placeholder_match in context and len(context.split(placeholder_match)) > 1 else ''
        after_text = after_text[:50].strip()
        
        # Look for parenthetical hints: "_____ (explanation)"
        paren_match = re.search(r'^\s*\(([^)]+)\)', after_text)
        if paren_match:
            hint = paren_match.group(1).strip()
            if 3 <= len(hint) <= 40:
                # Clean up quotes and other marks
                hint = re.sub(r'^["\']+|["\']+$', '', hint)
                return ' '.join(word.capitalize() for word in hint.split())
        
        # If starts with $, it's likely a monetary amount
        if placeholder_match.startswith('$'):
            return 'Purchase Amount'
        elif 'company' in before_text.lower()[-40:]:
            return 'Company Information'
        elif 'investor' in before_text.lower()[-40:]:
            return 'Investor Information'
        elif 'name' in before_text.lower()[-20:]:
            return 'Name'
        elif 'title' in before_text.lower()[-20:]:
            return 'Title/Position'
        elif 'date' in before_text.lower()[-20:]:
            return 'Date'
        
        # Default names based on length and type
        if len(placeholder_match) > 15:
            return 'Required Information'
        elif placeholder_match.startswith('_'):
            return 'Required Field'
        return 'Value'
    
    def group_related_placeholders(self, placeholders: List[Dict]) -> Dict[str, List[Dict]]:
        """
        Group related placeholders together for better UX.
        
        Args:
            placeholders (List[Dict]): List of placeholders
            
        Returns:
            Dict[str, List[Dict]]: Grouped placeholders
        """
        groups = {
            'company_info': [],
            'personal_info': [],
            'dates': [],
            'financial': [],
            'contact': [],
            'addresses': [],
            'legal_terms': [],
            'other': []
        }
        
        for placeholder in placeholders:
            placeholder_type = placeholder.get('type', 'text')
            name_lower = placeholder.get('name', '').lower()
            
            # Categorize based on type and name
            if placeholder_type == 'company':
                groups['company_info'].append(placeholder)
            elif placeholder_type == 'person':
                groups['personal_info'].append(placeholder)
            elif placeholder_type == 'date':
                groups['dates'].append(placeholder)
            elif placeholder_type in ['amount', 'percentage', 'number']:
                groups['financial'].append(placeholder)
            elif placeholder_type == 'contact':
                groups['contact'].append(placeholder)
            elif placeholder_type == 'address':
                groups['addresses'].append(placeholder)
            elif any(term in name_lower for term in ['governing', 'jurisdiction', 'law', 'notice']):
                groups['legal_terms'].append(placeholder)
            else:
                groups['other'].append(placeholder)
        
        # Remove empty groups
        groups = {k: v for k, v in groups.items() if v}
        
        logger.info(f"Grouped {len(placeholders)} placeholders into {len(groups)} categories")
        return groups
    
    def suggest_placeholder_values(self, placeholder: Dict,
                                  context: Optional[Dict] = None) -> List[str]:
        """
        Suggest possible values for a placeholder based on type and context.
        
        Args:
            placeholder (Dict): Placeholder information
            context (Optional[Dict]): Additional context for suggestions
            
        Returns:
            List[str]: List of suggested values
        """
        suggestions = []
        placeholder_type = placeholder.get('type', 'text')
        name_lower = placeholder.get('name', '').lower()
        
        # Date suggestions
        if placeholder_type == 'date':
            today = datetime.now()
            
            if 'effective' in name_lower or 'start' in name_lower:
                # Suggest today's date
                suggestions.append(today.strftime('%m/%d/%Y'))
            elif 'expiration' in name_lower or 'end' in name_lower or 'termination' in name_lower:
                # Suggest dates in the future
                future_dates = [
                    today + timedelta(days=30),   # 30 days
                    today + timedelta(days=90),   # 90 days
                    today + timedelta(days=365),  # 1 year
                ]
                for date in future_dates:
                    suggestions.append(date.strftime('%m/%d/%Y'))
        
        # Company suggestions from context
        elif placeholder_type == 'company':
            if context and 'recent_companies' in context:
                suggestions.extend(context['recent_companies'][:3])
            else:
                # Common company suffixes
                suggestions = ['[Company Name], Inc.', '[Company Name] LLC', '[Company Name] Corporation']
        
        # Percentage suggestions
        elif placeholder_type == 'percentage':
            if 'discount' in name_lower:
                suggestions = ['20%', '15%', '10%', '25%']
            elif 'interest' in name_lower:
                suggestions = ['5%', '7%', '10%', '12%']
            elif 'commission' in name_lower:
                suggestions = ['5%', '10%', '15%', '20%']
            else:
                suggestions = ['10%', '25%', '50%']
        
        # Amount suggestions
        elif placeholder_type == 'amount':
            if 'valuation' in name_lower:
                suggestions = ['$5,000,000', '$10,000,000', '$25,000,000']
            elif 'investment' in name_lower or 'purchase' in name_lower:
                suggestions = ['$100,000', '$250,000', '$500,000', '$1,000,000']
            elif 'fee' in name_lower:
                suggestions = ['$1,000', '$5,000', '$10,000']
            else:
                suggestions = ['$10,000', '$50,000', '$100,000']
        
        # State suggestions (for incorporation)
        elif placeholder_type == 'address' and 'state' in name_lower:
            if 'incorporation' in name_lower:
                # Common states for incorporation
                suggestions = ['Delaware', 'Nevada', 'Wyoming', 'California', 'New York']
            else:
                # General state suggestions
                suggestions = ['California', 'New York', 'Texas', 'Florida', 'Illinois']
        
        # Title suggestions
        elif 'title' in name_lower or 'position' in name_lower:
            suggestions = ['Chief Executive Officer', 'President', 'Chief Financial Officer',
                          'Vice President', 'Secretary', 'Director']
        
        # Number of shares suggestions
        elif 'shares' in name_lower:
            suggestions = ['1,000,000', '10,000,000', '100,000', '500,000']
        
        return suggestions
    
    def validate_placeholder_format(self, placeholder: Dict) -> Dict[str, Any]:
        """
        Validate that a placeholder is properly formatted.
        
        Args:
            placeholder (Dict): Placeholder to validate
            
        Returns:
            Dict: Validation results
        """
        issues = []
        warnings = []
        
        # Check required fields
        required_fields = ['key', 'name', 'original', 'type']
        for field in required_fields:
            if field not in placeholder:
                issues.append(f"Missing required field: {field}")
        
        # Check key format
        if 'key' in placeholder:
            key = placeholder['key']
            if not re.match(r'^[a-z0-9_]+$', key):
                warnings.append(f"Key contains invalid characters: {key}")
        
        # Check name
        if 'name' in placeholder:
            name = placeholder['name']
            if len(name) < 2:
                warnings.append("Placeholder name is too short")
            if len(name) > 50:
                warnings.append("Placeholder name is too long")
        
        # Check type
        if 'type' in placeholder:
            valid_types = ['company', 'person', 'date', 'amount', 'percentage',
                          'address', 'contact', 'number', 'signature', 'text']
            if placeholder['type'] not in valid_types:
                warnings.append(f"Unknown type: {placeholder['type']}")
        
        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'warnings': warnings
        }