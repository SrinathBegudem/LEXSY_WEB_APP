"""
Services Package
================
Core business logic services for document processing, AI interactions,
and placeholder detection.

This package contains:
- DocumentProcessor: Handles DOCX parsing and generation
- AIService: Manages conversational AI for filling documents
- PlaceholderDetector: Identifies and analyzes placeholders

Author: Legal Tech Solutions
Date: October 2025
Version: 1.0.0
"""

from .document_processor import DocumentProcessor
from .ai_service import AIService
from .placeholder_detector import PlaceholderDetector

__all__ = [
    'DocumentProcessor',
    'AIService',
    'PlaceholderDetector'
]

__version__ = '1.0.0'
