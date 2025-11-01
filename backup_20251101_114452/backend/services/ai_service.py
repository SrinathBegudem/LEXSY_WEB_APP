"""
AI Service
==========
Handles conversational AI interactions for filling document placeholders.
Uses Groq API (FREE) with llama-3.1-70b model for intelligent conversations.

This module provides:
- Conversation initialization and context management
- Intelligent question generation for placeholders
- Input validation based on field types
- Natural language processing for user responses
- Fallback to mock responses when API is unavailable

Author: Legal Tech Solutions
Date: October 2025
Version: 1.0.0
"""

import os
import json
import re
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from dateutil import parser as date_parser

# Import Groq client
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False
    logging.warning("Groq package not installed. Using mock AI responses.")

# Configure logging
logger = logging.getLogger(__name__)


class AIService:
    """
    AI Service for managing conversational document filling.
    
    This service:
    - Manages conversation flow for filling placeholders
    - Generates contextual questions based on field types
    - Validates and formats user inputs
    - Maintains conversation history and context
    """
    
    def __init__(self):
        """
        Initialize the AI service with Groq API or mock fallback.
        """
        self.provider = self._initialize_provider()
        self.conversation_history = []
        self.system_prompt = self._create_system_prompt()
        logger.info(f"AIService initialized with provider: {self.provider}")
    
    def _initialize_provider(self) -> str:
        """
        Initialize the AI provider based on available API keys.
        
        Returns:
            str: Provider name ('groq' or 'mock')
        """
        groq_key = os.environ.get('GROQ_API_KEY')
        
        if groq_key and GROQ_AVAILABLE:
            try:
                self.client = Groq(api_key=groq_key)
                logger.info("Using Groq AI provider")
                return 'groq'
            except Exception as e:
                logger.error(f"Failed to initialize Groq client: {str(e)}")
                return 'mock'
        else:
            if not groq_key:
                logger.warning("No GROQ_API_KEY found in environment variables")
            logger.info("Using mock AI provider")
            return 'mock'
    
    def _create_system_prompt(self) -> str:
        """
        Create the system prompt for the AI assistant.
        
        Returns:
            str: System prompt defining the AI's role and behavior
        """
        return """You are a professional legal document assistant helping users fill out legal documents.

Your role:
1. Ask clear, specific questions about each placeholder
2. Provide helpful context when the field purpose isn't obvious
3. Validate responses to ensure they're appropriate
4. Guide users step-by-step through the document
5. Be professional yet friendly and approachable

When asking about placeholders:
- Explain what the field is for if needed
- Provide format examples (e.g., "MM/DD/YYYY" for dates)
- Ask follow-up questions if responses are unclear
- Confirm formatted values with the user
- Be encouraging and patient

Important guidelines:
- Keep questions concise and clear
- Use simple language, avoid legal jargon
- Be helpful but not overly verbose
- Maintain a professional tone
- Focus on one field at a time"""
    
    def initialize_conversation(self, document_content: Dict, placeholders: List[Dict]) -> Dict:
        """
        Initialize a new conversation context for document filling.
        
        Args:
            document_content (Dict): Parsed document content
            placeholders (List[Dict]): List of detected placeholders
            
        Returns:
            Dict: Conversation context with metadata
        """
        # Identify document type from content
        document_type = self._identify_document_type(document_content)
        
        # Categorize placeholders by type
        categories = self._categorize_placeholders(placeholders)
        
        # Create conversation context
        context = {
            'document_type': document_type,
            'total_placeholders': len(placeholders),
            'placeholder_categories': categories,
            'started_at': datetime.now().isoformat(),
            'estimated_time_minutes': max(1, len(placeholders) // 2),  # Rough estimate
            'current_section': None
        }
        
        # Initialize conversation history
        self.conversation_history = [
            {
                'role': 'system',
                'content': self.system_prompt
            },
            {
                'role': 'system',
                'content': f"""Document Information:
- Type: {document_type}
- Total fields: {context['total_placeholders']}
- Categories: {', '.join(categories)}

Start with a friendly greeting and explain the process."""
            }
        ]
        
        logger.info(f"Initialized conversation for {document_type} with {len(placeholders)} placeholders")
        return context
    
    def _identify_document_type(self, content: Dict) -> str:
        """
        Identify the type of legal document based on content.
        
        Args:
            content (Dict): Document content
            
        Returns:
            str: Identified document type
        """
        text = content.get('raw_text', '').lower()
        
        # Common legal document patterns
        document_types = {
            'SAFE Agreement': ['safe', 'simple agreement for future equity', 'valuation cap'],
            'Non-Disclosure Agreement': ['non-disclosure', 'nda', 'confidential', 'proprietary information'],
            'Employment Agreement': ['employment', 'employee', 'compensation', 'benefits', 'termination'],
            'Service Agreement': ['services', 'contractor', 'deliverables', 'scope of work'],
            'Purchase Agreement': ['purchase', 'sale', 'buyer', 'seller', 'purchase price'],
            'Terms of Service': ['terms of service', 'terms and conditions', 'user agreement'],
            'Privacy Policy': ['privacy policy', 'personal information', 'data protection'],
            'Partnership Agreement': ['partnership', 'partners', 'profit sharing', 'capital contribution'],
            'Licensing Agreement': ['license', 'licensing', 'royalty', 'intellectual property'],
            'Loan Agreement': ['loan', 'lender', 'borrower', 'interest rate', 'repayment']
        }
        
        # Check for document type markers
        for doc_type, keywords in document_types.items():
            if any(keyword in text for keyword in keywords):
                return doc_type
        
        return 'Legal Agreement'
    
    def _categorize_placeholders(self, placeholders: List[Dict]) -> List[str]:
        """
        Categorize placeholders by their type/purpose.
        
        Args:
            placeholders (List[Dict]): List of placeholders
            
        Returns:
            List[str]: List of unique categories
        """
        categories = set()
        
        for placeholder in placeholders:
            name = placeholder.get('name', '').lower()
            
            if any(term in name for term in ['company', 'entity', 'corporation', 'business']):
                categories.add('Company Information')
            elif any(term in name for term in ['name', 'person', 'individual', 'party']):
                categories.add('Personal Information')
            elif any(term in name for term in ['date', 'time', 'deadline', 'effective', 'expiration']):
                categories.add('Dates and Deadlines')
            elif any(term in name for term in ['amount', 'price', 'fee', 'payment', 'valuation', '$']):
                categories.add('Financial Terms')
            elif any(term in name for term in ['address', 'location', 'jurisdiction', 'state', 'city']):
                categories.add('Locations')
            elif any(term in name for term in ['email', 'phone', 'contact', 'telephone']):
                categories.add('Contact Information')
            elif any(term in name for term in ['percentage', 'rate', 'discount', '%']):
                categories.add('Percentages and Rates')
            else:
                categories.add('Other Terms')
        
        return sorted(list(categories))
    
    def get_greeting_message(self, placeholders: List[Dict]) -> str:
        """
        Generate an initial greeting message with first field question.
        
        Args:
            placeholders (List[Dict]): List of placeholders
            
        Returns:
            str: Greeting message with first field question
        """
        num_fields = len(placeholders)
        estimated_time = max(1, num_fields // 2)
        
        # Get the first field name
        first_field = placeholders[0].get('name', 'Field') if placeholders else 'Field'
        
        greeting = f"""👋 **Welcome to Lexsy Document Assistant!**

I've detected **{num_fields} field{'s' if num_fields != 1 else ''}** in your document that need{'s' if num_fields == 1 else ''} to be completed.

⏱️ Estimated time: {estimated_time} minute{'s' if estimated_time != 1 else ''}

I'll guide you through each field, validate your responses, and help ensure everything is filled correctly.

---

"""
        
        # Add the first field question
        first_question = self._generate_placeholder_question(placeholders[0], 0, num_fields)
        
        return greeting + first_question
    
    def process_message(self, user_message: str, placeholders: List[Dict],
                       filled_values: Dict, current_index: int,
                       ai_context: Dict) -> Dict:
        """
        Process a user message and generate appropriate response.
        
        Args:
            user_message (str): User's input message
            placeholders (List[Dict]): List of all placeholders
            filled_values (Dict): Already filled values
            current_index (int): Current placeholder index (represents which field we're asking about)
            ai_context (Dict): Conversation context
            
        Returns:
            Dict: Response with message and metadata
        """
        # CRITICAL FIX: Use current_index directly, not len(filled_values)
        # current_index represents which field we're currently asking about
        # len(filled_values) can be different if fields are auto-filled or edited
        
        # Find the next unfilled placeholder starting from current_index
        # This handles edge cases where current_index might point to an already-filled field
        actual_index = current_index
        while actual_index < len(placeholders):
            ph = placeholders[actual_index]
            ph_id = ph.get('id', ph['key'])
            ph_key = ph.get('key')
            
            # Check if this placeholder is already filled
            is_filled = (ph_id in filled_values or ph_key in filled_values)
            
            if not is_filled:
                break
            
            actual_index += 1
        
        # Check if we're still filling placeholders
        if actual_index < len(placeholders):
            current_placeholder = placeholders[actual_index]
            
            # Validate the user's response for current placeholder
            validation_result = self._validate_placeholder_value(
                user_message,
                current_placeholder
            )
            
            if validation_result['valid']:
                # Value is valid - prepare response for next placeholder
                # Use ID as primary identifier, fall back to key if not present
                placeholder_id = current_placeholder.get('id', current_placeholder['key'])
                
                response = {
                    'placeholder_filled': True,
                    'placeholder_key': placeholder_id,  # Use ID instead of key
                    'value': validation_result['processed_value']
                }
                
                # Handle auto-fills for duplicate fields with the same name
                # If a field appears multiple times (e.g., "Disclosing Party Address" in Field 3 and Field 10),
                # automatically fill all occurrences with the same value
                current_name = current_placeholder['name']
                current_normalized = self._normalize_field_name(current_name)
                
                response['auto_fills'] = []
                auto_filled_count = 0
                
                for ph in placeholders:
                    # Match by exact name (case-insensitive) and normalized name for better matching
                    ph_name = ph.get('name', '')
                    ph_normalized = self._normalize_field_name(ph_name)
                    ph_id = ph.get('id', ph['key'])
                    
                    # Skip the current placeholder and already filled ones
                    if ph_id == placeholder_id:
                        continue
                    
                    # Match if exact name matches OR normalized name matches
                    # This handles cases like "Disclosing Party Address" vs "disclosing party address"
                    name_matches = (
                        ph_name.lower() == current_name.lower() or 
                        ph_normalized == current_normalized
                    )
                    
                    if name_matches:
                        # Check if this placeholder is already filled
                        is_already_filled = (
                            ph_id in filled_values or 
                            ph['key'] in filled_values
                        )
                        
                        if not is_already_filled:
                            response['auto_fills'].append({
                                'key': ph_id,
                                'value': validation_result['processed_value'],
                                'name': ph_name  # Include name for logging
                            })
                            auto_filled_count += 1
                
                if response['auto_fills']:
                    auto_fill_names = [af.get('name', 'unknown') for af in response['auto_fills']]
                    logger.info(
                        f"Auto-filling {auto_filled_count} other occurrence(s) of '{current_name}': "
                        f"{', '.join(auto_fill_names)}"
                    )
                
                # Create a comprehensive set of all filled keys (including current and auto-fills)
                all_filled_keys = set(filled_values.keys())
                all_filled_keys.add(placeholder_id)  # Current placeholder
                for auto_fill in response.get('auto_fills', []):
                    all_filled_keys.add(auto_fill['key'])
                    # Also add by key for compatibility
                    auto_fill_ph = next((p for p in placeholders if p.get('id', p['key']) == auto_fill['key']), None)
                    if auto_fill_ph:
                        all_filled_keys.add(auto_fill_ph['key'])
                
                # Find the next unfilled placeholder (accounting for auto-fills)
                # CRITICAL: Scan sequentially to find the first unfilled placeholder
                # This handles edge cases where fields are out of order or auto-filled fields appear earlier
                next_index = None
                scanned_count = 0
                for i, ph in enumerate(placeholders):
                    scanned_count += 1
                    ph_id = ph.get('id', ph['key'])
                    ph_key = ph.get('key')
                    
                    # Check if this placeholder is already filled (including auto-fills)
                    is_filled = (
                        ph_id in all_filled_keys or 
                        ph_key in all_filled_keys or
                        ph_id in filled_values or 
                        ph_key in filled_values
                    )
                    
                    if not is_filled:
                        next_index = i
                        logger.debug(
                            f"Next unfilled placeholder at index {i}: '{ph.get('name', 'Unknown')}' "
                            f"(scanned {scanned_count}/{len(placeholders)} placeholders)"
                        )
                        break
                
                # Store next_index in response for app.py to use
                response['next_index'] = next_index
                
                if next_index is not None:
                    next_placeholder = placeholders[next_index]
                    response['message'] = self._generate_placeholder_question(
                        next_placeholder,
                        next_index,
                        len(placeholders)
                    )
                else:
                    # All placeholders filled
                    response['message'] = self._generate_completion_message(len(placeholders))
                    logger.info(f"All {len(placeholders)} placeholders have been filled (including {auto_filled_count} auto-filled)")
                
                return response
            else:
                # Invalid value - use validation error message directly
                # Skip AI enhancement for number/month fields to avoid confusion
                error_msg = validation_result['error_message']
                placeholder_name = current_placeholder.get('name', '')
                
                # Only use AI enhancement for non-number fields to avoid confusion
                # Number/month fields already have clear error messages
                is_number_field = (
                    current_placeholder.get('type') == 'number' or
                    'month' in placeholder_name.lower() or
                    'term' in placeholder_name.lower()
                )
                
                if not is_number_field and self.provider == 'groq' and GROQ_AVAILABLE:
                    try:
                        ai_error_prompt = f"""User entered invalid input "{user_message}" for field "{placeholder_name}".
                        
The validation error is: {error_msg}

Generate a friendly, helpful message that:
- Acknowledges their mistake positively
- Clearly explains what format/value is expected
- Provides examples
- Encourages them to try again

Keep it concise (1-2 sentences) and professional. Return ONLY the message."""

                        ai_enhanced_msg = self.get_ai_response(
                            prompt=ai_error_prompt,
                            context="You are a friendly assistant helping users fill legal documents. Make error messages helpful and encouraging."
                        )
                        
                        if ai_enhanced_msg and len(ai_enhanced_msg) < 500:
                            error_msg = ai_enhanced_msg.strip()
                            logger.debug(f"AI-enhanced error message generated")
                    except Exception as e:
                        logger.debug(f"AI error enhancement failed: {e}")
                
                return {
                    'placeholder_filled': False,
                    'message': error_msg
                }
        
        # All placeholders already filled
        return {
            'placeholder_filled': False,
            'message': "Great! All fields have been filled. You can now preview your document and download the completed version."
        }
    
    def _handle_first_interaction(self, first_placeholder: Dict) -> Dict:
        """
        Handle the first interaction with user.
        
        Args:
            first_placeholder (Dict): First placeholder to fill
            
        Returns:
            Dict: Response with greeting and first question
        """
        greeting = self.get_greeting_message([first_placeholder])
        question = self._generate_placeholder_question(first_placeholder, 0, 1)
        
        return {
            'placeholder_filled': False,
            'message': f"{greeting}\n\n{question}"
        }
    
    def _generate_placeholder_question(self, placeholder: Dict, 
                                      current: int, total: int) -> str:
        """
        Generate a contextual question for a specific placeholder.
        Uses AI for more natural, engaging questions.
        
        Args:
            placeholder (Dict): Placeholder information
            current (int): Current position
            total (int): Total number of placeholders
            
        Returns:
            str: Question for the placeholder
        """
        name = placeholder.get('name', 'Field')
        placeholder_type = placeholder.get('type', 'text')
        placeholder_lower = name.lower()
        
        # Progress indicator with helpful hint
        progress = f"📝 **Field {current + 1} of {total}: {name}**\n\n"
        
        # If AI is enabled, try to generate a more engaging, natural question
        if self.provider == 'groq' and GROQ_AVAILABLE:
            try:
                # Create a prompt for AI to generate contextual question
                ai_prompt = f"""Generate a friendly, professional question to ask for filling the field "{name}" which is of type "{placeholder_type}".

Guidelines:
- Be concise (one sentence)
- Be friendly and professional
- Provide format examples if needed
- Don't be overly verbose
- Add appropriate emoji if relevant

Return ONLY the question, no prefixes or extra text."""

                ai_question = self.get_ai_response(
                    prompt=ai_prompt,
                    context="You are a helpful legal document assistant. Generate conversational questions for document fields."
                )
                
                # Use AI-generated question if it looks reasonable
                # Allow longer questions - increased limit for better AI responses
                if ai_question and len(ai_question) < 1000 and '?' in ai_question:
                    logger.debug(f"Using AI-generated question for {name}")
                    return progress + ai_question.strip()
                    
            except Exception as e:
                logger.warning(f"AI question generation failed for {name}: {e}. Using template.")
        
        # Fallback to template-based questions
        if placeholder_type == 'company':
            question = f"💼 Please provide the full legal name of the company, including any corporate designation (Inc., LLC, Corp., etc.)."
        
        elif placeholder_type == 'date':
            if 'incorporation' in placeholder_lower:
                question = f"📅 When was the company incorporated? Please use MM/DD/YYYY format."
            elif 'effective' in placeholder_lower or 'agreement' in placeholder_lower:
                question = f"📅 What is the effective date for this agreement? Please use MM/DD/YYYY format."
            else:
                question = f"📅 Please provide the date in MM/DD/YYYY format."
        
        elif placeholder_type == 'amount':
            if 'purchase' in placeholder_lower:
                question = f"💰 Please enter the purchase amount (e.g., 100000 or $100,000)."
            elif 'valuation' in placeholder_lower:
                question = f"💰 Please enter the valuation cap amount (e.g., 5000000 or $5,000,000)."
            else:
                question = f"💰 Please enter the amount (numbers only, $ symbol will be added automatically)."
        
        elif placeholder_type == 'percentage':
            question = f"📊 Please enter the percentage or rate (e.g., 20 for 20%)."
        
        elif placeholder_type == 'contact':
            question = f"📧 Please provide a valid email address."
        
        elif placeholder_type == 'address':
            # Special handling for specific address types - CHECK NAME FIRST before generic 'state' match
            if 'state of incorporation' in placeholder_lower:
                question = f"📍 Please provide the **state of incorporation** (e.g., Delaware, California, or DE, CA)."
            elif 'governing law' in placeholder_lower or 'governing law jurisdiction' in placeholder_lower:
                question = f"⚖️ Please provide the **governing law jurisdiction** (e.g., State of Delaware, California)."
            elif 'jurisdiction' in placeholder_lower:
                question = f"⚖️ Please provide the **jurisdiction** (e.g., State of Delaware, California)."
            elif 'state' in placeholder_lower:
                question = f"📍 Please provide the **state name or abbreviation** (e.g., Delaware, DE)."
            else:
                question = f"📍 Please provide the **complete address**."
        
        elif placeholder_type == 'person':
            if 'investor' in placeholder_lower:
                question = f"👤 Please provide the full name of the investor."
            elif 'first' in placeholder_lower:
                question = f"👤 Please provide the first name."
            elif 'last' in placeholder_lower:
                question = f"👤 Please provide the last name."
            elif 'title' in placeholder_lower:
                question = f"👤 Please provide the person's title (e.g., CEO, Director, Manager)."
            else:
                question = f"👤 Please provide the full name."
        
        elif placeholder_type == 'number':
            question = f"🔢 Please provide the number."
        
        elif placeholder_type == 'text':
            # Provide context-specific hints for text fields
            if 'title' in placeholder_lower:
                question = f"📝 Please provide the title or designation (e.g., CEO, CFO, Director)."
            elif 'name' in placeholder_lower and len(placeholder_lower) < 10:
                question = f"👤 Please provide the name requested for this field."
            elif 'value' in placeholder_lower:
                question = f"📝 Please provide the value or information for: **{name}**."
            else:
                question = f"📝 Please provide the information for: **{name}**."
        
        else:
            # Generic question with field name emphasis
            question = f"📝 Please provide the information for: **{name}**."
        
        return progress + question
    
    def _validate_placeholder_value(self, value: str, placeholder: Dict) -> Dict:
        """
        Validate and format user input for a placeholder.
        
        Args:
            value (str): User input value
            placeholder (Dict): Placeholder information
            
        Returns:
            Dict: Validation result with processed value or error message
        """
        name = placeholder.get('name', '').lower()
        placeholder_type = placeholder.get('type', 'text')
        value = value.strip()
        
        # Check for empty values
        if not value:
            return {
                'valid': False,
                'error_message': "This field is required. Please provide a value."
            }
        
        # Email validation
        if placeholder_type == 'contact' or 'email' in name:
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, value):
                return {
                    'valid': False,
                    'error_message': "❌ That doesn't appear to be a valid email address.\n\nPlease provide a valid email address:"
                }
            # Valid email - return it
            return {'valid': True, 'processed_value': value}
        
        # Number validation for fields like "Term Months" - MUST come before date validation
        # to prevent "12" from being treated as a date
        # Check both type and name patterns to handle cases where type detection failed
        is_month_number_field = (
            placeholder_type == 'number' or 
            ('month' in name and any(word in name for word in ['term', 'number', 'count', 'quantity', 'duration', 'period'])) or
            ('term month' in name) or ('months' in name and 'date' not in name)
        )
        
        if is_month_number_field:
            # Remove commas for processing
            cleaned_value = value.replace(',', '').strip()
            
            try:
                number = float(cleaned_value)
                
                # Ensure it's a positive integer for months/terms
                if number <= 0:
                    return {
                        'valid': False,
                        'error_message': f"❌ The \"{placeholder.get('name', 'Term Months')}\" field should be a positive number of months (e.g., 6, 12, or 24)."
                    }
                
                # Format as integer if it's a whole number
                if number == int(number):
                    value = str(int(number))
                else:
                    value = str(number)
                
                return {'valid': True, 'processed_value': value}
                
            except ValueError:
                return {
                    'valid': False,
                    'error_message': f"❌ The \"{placeholder.get('name', 'Term Months')}\" field expects a number (e.g., 6, 12, or 24 months), not a date or text."
                }
        
        # Date validation and formatting
        elif placeholder_type == 'date' or ('date' in name and 'month' not in name):
            # First validate MM/DD/YYYY format strictly
            date_formats = [
                r'^(0[1-9]|1[0-2])/(0[1-9]|[12][0-9]|3[01])/(\d{4})$',  # MM/DD/YYYY
            ]
            
            # Check if already in correct format
            match = re.match(date_formats[0], value)
            if match:
                # Validate month and day ranges
                month = int(match.group(1))
                day = int(match.group(2))
                if month < 1 or month > 12:
                    return {
                        'valid': False,
                        'error_message': "❌ Invalid month. Please provide a date in MM/DD/YYYY format (month must be 01-12)."
                    }
                if day < 1 or day > 31:
                    return {
                        'valid': False,
                        'error_message': "❌ Invalid day. Please provide a date in MM/DD/YYYY format (day must be 01-31)."
                    }
                return {'valid': True, 'processed_value': value}
            
            # Don't try to auto-correct invalid dates
            return {
                'valid': False,
                'error_message': "❌ Please provide the date in MM/DD/YYYY format."
            }
        
        # Address/State validation - MUST come before amount check to avoid false matches
        elif placeholder_type == 'address' or ('state' in name) or ('jurisdiction' in name):
            # Special handling for state/jurisdiction fields
            if ('state' in name) or ('jurisdiction' in name):
                # Accept any state name or jurisdiction - standardize common abbreviations
                state_map = {
                    'de': 'Delaware',
                    'ca': 'California',
                    'ny': 'New York',
                    'tx': 'Texas',
                    'fl': 'Florida',
                    'il': 'Illinois',
                    'nv': 'Nevada',
                    'wy': 'Wyoming',
                }
                
                value_lower = value.lower().strip()
                
                # Check if it's a common abbreviation
                if value_lower in state_map:
                    value = state_map[value_lower]
                elif len(value) == 2:
                    # Two-letter abbreviation - keep uppercase
                    value = value.upper()
                else:
                    # Full name - capitalize properly
                    value = value.title()
                
                return {'valid': True, 'processed_value': value}
            else:
                # Generic address validation
                # Basic text cleanup
                value = ' '.join(value.split())  # Normalize whitespace
                return {'valid': True, 'processed_value': value}
        
        # Amount/currency validation
        elif placeholder_type == 'amount' or any(x in name for x in ['amount', 'price', 'valuation', 'fee', '$']):
            # Remove common formatting characters
            cleaned_value = re.sub(r'[,$]', '', value)
            
            try:
                # Validate it's a number
                amount = float(cleaned_value)
                
                # Format with currency and commas
                if amount >= 1000:
                    formatted_amount = f"${amount:,.0f}"
                else:
                    formatted_amount = f"${amount:.2f}"
                
                # Ensure $ symbol
                if not value.startswith('$'):
                    value = formatted_amount
                else:
                    value = value.replace(',', '')
                    # Add commas for thousands
                    if amount >= 1000:
                        value = formatted_amount
                
                return {'valid': True, 'processed_value': value}
                
            except ValueError:
                return {
                    'valid': False,
                    'error_message': "❌ Please provide a valid amount (numbers only, $ symbol optional)."
                }
        
        # Percentage validation
        elif placeholder_type == 'percentage' or any(x in name for x in ['rate', 'discount', 'percent', '%']):
            # Remove % symbol for processing
            cleaned_value = value.replace('%', '').strip()
            
            try:
                percentage = float(cleaned_value)
                
                # Format appropriately
                if percentage > 1 and percentage <= 100:
                    # Assume it's already a percentage
                    value = f"{percentage}%"
                elif percentage <= 1:
                    # Assume it's a decimal, convert to percentage
                    value = f"{percentage * 100}%"
                else:
                    # Over 100%
                    value = f"{percentage}%"
                
                return {'valid': True, 'processed_value': value}
                
            except ValueError:
                return {
                    'valid': False,
                    'error_message': "❌ Please provide a valid percentage (e.g., 20 or 20%)."
                }
        
        # Phone number validation
        elif 'phone' in name or 'telephone' in name:
            # Remove common formatting characters
            cleaned_phone = re.sub(r'[\s\-\(\)\+]', '', value)
            
            # Check if it's a valid length (10-15 digits typically)
            if not cleaned_phone.isdigit() or len(cleaned_phone) < 10 or len(cleaned_phone) > 15:
                return {
                    'valid': False,
                    'error_message': "❌ Please provide a valid phone number (10-15 digits)."
                }
            
            # Format US phone numbers
            if len(cleaned_phone) == 10:
                value = f"({cleaned_phone[:3]}) {cleaned_phone[3:6]}-{cleaned_phone[6:]}"
            
            return {'valid': True, 'processed_value': value}
        
        # Number validation (general case - for shares, quantities, etc.)
        elif placeholder_type == 'number' or ('number' in name or 'shares' in name or 'quantity' in name):
            # Remove commas for processing
            cleaned_value = value.replace(',', '')
            
            try:
                number = float(cleaned_value)
                
                # Format with commas if it's a large number
                if number >= 1000 and number == int(number):
                    value = f"{int(number):,}"
                
                return {'valid': True, 'processed_value': value}
                
            except ValueError:
                return {
                    'valid': False,
                    'error_message': "❌ Please provide a valid number."
                }
        
        # Default validation - just ensure it's not empty
        else:
            # Basic text cleanup
            value = ' '.join(value.split())  # Normalize whitespace
            
            return {'valid': True, 'processed_value': value}
    
    def _normalize_field_name(self, name: str) -> str:
        """
        Normalize a field name for comparison (handles case, spaces, punctuation).
        Used for matching duplicate fields that should be auto-filled.
        
        Args:
            name (str): Field name to normalize
            
        Returns:
            str: Normalized field name for comparison
        """
        if not name:
            return ''
        
        # Convert to lowercase and remove extra whitespace
        normalized = name.lower().strip()
        
        # Replace multiple spaces/underscores with single space
        normalized = re.sub(r'[\s_]+', ' ', normalized)
        
        # Remove common punctuation but keep important separators
        normalized = re.sub(r'[^\w\s]', '', normalized)
        
        return normalized
    
    def _generate_completion_message(self, total_placeholders: int) -> str:
        """
        Generate a completion message when all fields are filled.
        
        Args:
            total_placeholders (int): Total number of placeholders filled
            
        Returns:
            str: Completion message
        """
        return f"""🎉 **Perfect! All {total_placeholders} fields have been completed.**

Your document is ready to review and download.

**Next Steps:**

✅ Review the document preview to verify all information is correct

✅ Click the "Complete Document" button to finalize

✅ Download your completed document in .docx format

Thank you for using Lexsy Document Assistant!"""
    
    def analyze_field_context(self, placeholder: Dict, document_context: str) -> Dict[str, str]:
        """
        Use AI to analyze field context and suggest better field name and question.
        
        Args:
            placeholder (Dict): Placeholder information
            document_context (str): Surrounding document context
            
        Returns:
            Dict with 'suggested_name', 'suggested_question', 'field_type'
        """
        if self.provider == 'groq' and GROQ_AVAILABLE:
            try:
                # Create a focused prompt for field analysis
                field_name = placeholder.get('name', 'Unknown Field')
                field_context = placeholder.get('context', document_context[:200])
                original_placeholder = placeholder.get('original', '')
                
                analysis_prompt = f"""Analyze this placeholder field from a legal document and suggest:
1. A clear, descriptive field name (max 3-4 words)
2. A helpful question to ask the user
3. The most likely field type (company, person, date, amount, address, contact, number, text)

Field Information:
- Current name: "{field_name}"
- Placeholder text: "{original_placeholder}"
- Context: "{field_context}"

Respond in this exact JSON format:
{{
  "suggested_name": "Clear Field Name",
  "suggested_question": "What information should be entered here?",
  "field_type": "text"
}}

Be specific and helpful. If the field name is unclear (like "Field Value" or "_________"), infer from context."""
                
                # Get AI analysis
                response = self.client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {'role': 'system', 'content': 'You are a legal document analysis assistant. Provide accurate, specific field analysis in JSON format.'},
                        {'role': 'user', 'content': analysis_prompt}
                    ],
                    temperature=0.2,
                    max_tokens=200,
                    response_format={"type": "json_object"}
                )
                
                # Parse JSON response
                import json
                analysis = json.loads(response.choices[0].message.content)
                
                return {
                    'suggested_name': analysis.get('suggested_name', field_name),
                    'suggested_question': analysis.get('suggested_question', 'Please provide the value for this field.'),
                    'field_type': analysis.get('field_type', placeholder.get('type', 'text'))
                }
                
            except Exception as e:
                logger.warning(f"AI field analysis failed: {str(e)}, using fallback")
                # Fallback to current name
                return {
                    'suggested_name': placeholder.get('name', 'Field'),
                    'suggested_question': None,
                    'field_type': placeholder.get('type', 'text')
                }
        else:
            # Mock provider - return current name
            return {
                'suggested_name': placeholder.get('name', 'Field'),
                'suggested_question': None,
                'field_type': placeholder.get('type', 'text')
            }
    
    def get_ai_response(self, prompt: str, context: Optional[str] = None) -> str:
        """
        Get AI response from Groq or fallback to mock.
        
        Args:
            prompt (str): User prompt
            context (Optional[str]): Additional context
            
        Returns:
            str: AI response
        """
        if self.provider == 'groq' and GROQ_AVAILABLE:
            try:
                # Prepare messages
                messages = self.conversation_history.copy()
                
                if context:
                    messages.append({'role': 'system', 'content': context})
                
                messages.append({'role': 'user', 'content': prompt})
                
                # Call Groq API
                response = self.client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=messages,
                    temperature=0.3,  # Lower temperature for more consistent responses
                    max_tokens=1000,  # Increased for better responses
                    top_p=0.9
                )
                
                return response.choices[0].message.content
                
            except Exception as e:
                logger.error(f"Groq API error: {str(e)}")
                return self._get_mock_response(prompt)
        else:
            return self._get_mock_response(prompt)
    
    def _get_mock_response(self, prompt: str) -> str:
        """
        Generate a mock response when API is unavailable.
        
        Args:
            prompt (str): User prompt
            
        Returns:
            str: Mock response
        """
        # Simple mock responses for testing
        responses = {
            'greeting': "Welcome! I'll help you fill out this document step by step.",
            'date': "Please provide the date in MM/DD/YYYY format.",
            'email': "Please provide a valid email address.",
            'amount': "Please provide the amount (include currency symbol).",
            'company': "Please provide the full legal name of the company.",
            'name': "Please provide the full name.",
            'default': "Please provide the requested information for this field."
        }
        
        # Try to match prompt to response type
        prompt_lower = prompt.lower()
        
        if 'date' in prompt_lower:
            return responses['date']
        elif 'email' in prompt_lower:
            return responses['email']
        elif 'amount' in prompt_lower or '$' in prompt:
            return responses['amount']
        elif 'company' in prompt_lower:
            return responses['company']
        elif 'name' in prompt_lower:
            return responses['name']
        else:
            return responses['default']
    
    def format_value_for_display(self, value: str, placeholder_type: str) -> str:
        """
        Format a value for display in the document.
        
        Args:
            value (str): Raw value
            placeholder_type (str): Type of placeholder
            
        Returns:
            str: Formatted value
        """
        if placeholder_type == 'amount':
            # Ensure currency formatting
            if not value.startswith('$'):
                value = f"${value}"
        elif placeholder_type == 'percentage':
            # Ensure percentage sign
            if not value.endswith('%'):
                value = f"{value}%"
        elif placeholder_type == 'date':
            # Ensure consistent date format
            try:
                parsed_date = date_parser.parse(value)
                value = parsed_date.strftime('%B %d, %Y')  # "January 15, 2024"
            except:
                pass
        
        return value