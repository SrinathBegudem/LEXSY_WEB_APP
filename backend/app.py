"""
Legal Document Automation Platform - Main Flask Application
============================================================
This is the core Flask application that handles all API endpoints for document
processing, AI conversations, and document generation.

Author: Legal Tech Solutions
Date: October 2025
Version: 1.0.0
"""

import os
import json
import uuid
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional, Tuple

from flask import Flask, render_template, request, jsonify, send_file, session, make_response
from flask import Response, stream_with_context
from functools import wraps
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from dotenv import load_dotenv
import secrets

# Import our custom services
from services.document_processor import DocumentProcessor
from services.ai_service import AIService
from services.placeholder_detector import PlaceholderDetector
from services.session_manager import session_manager
from services.firebase_auth import verify_token, get_token_from_request

# Load environment variables from .env file
load_dotenv()

# Initialize Flask application
app = Flask(__name__)

# Configure Flask application
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(32))
app.config['MAX_CONTENT_LENGTH'] = int(os.environ.get('MAX_FILE_SIZE', 10 * 1024 * 1024))  # 10MB default
app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER', 'uploads')
app.config['PROCESSED_FOLDER'] = os.environ.get('PROCESSED_FOLDER', 'processed')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)  # Sessions expire after 24 hours

# Configure CORS for cross-origin requests
# Build allowed origins from environment for deployment flexibility
_default_local_origins = [
    'http://localhost:3000',
    'http://localhost:3001',
    'http://localhost:3002',
    'http://127.0.0.1:3000',
    'http://127.0.0.1:3001',
    'http://127.0.0.1:3002'
]

_env_origins = os.environ.get('CORS_ORIGINS', '').strip()
_allow_all = os.environ.get('CORS_ALLOW_ALL', 'false').lower() in ('1', 'true', 'yes')

if _allow_all:
    allowed_origins = '*'
else:
    allowed_origins = _default_local_origins.copy()
    if _env_origins:
        # Accept comma or whitespace separated list
        extra = [o.strip() for o in _env_origins.replace('\n', ',').split(',') if o.strip()]
        allowed_origins.extend(extra)

def cors_check(origin):
    """Check if origin is allowed. Accept all if wildcard is enabled."""
    if allowed_origins == '*':
        return True
    return origin in allowed_origins

CORS(
    app,
    origins=allowed_origins,
    origin_check=cors_check,
    supports_credentials=True,
    methods=['GET', 'POST', 'OPTIONS', 'PUT', 'DELETE'],
    allow_headers=['Content-Type', 'Authorization', 'X-Requested-With'],
    expose_headers=['Content-Type', 'Content-Disposition'],
    max_age=3600
)

# Configure logging with enhanced format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Log startup information
logger.info("=" * 60)
logger.info("🚀 LEXSY BACKEND STARTING")
logger.info("=" * 60)
logger.info(f"   Environment: {os.environ.get('FLASK_ENV', 'development')}")
logger.info(f"   Python Version: {os.sys.version.split()[0]}")
logger.info(f"   Port: {os.environ.get('PORT', '5001')}")
logger.info(f"   Upload Folder: {app.config['UPLOAD_FOLDER']}")
logger.info(f"   Max File Size: {app.config['MAX_CONTENT_LENGTH'] / (1024*1024):.1f} MB")
logger.info("=" * 60)

# Ensure required directories exist
for folder in [app.config['UPLOAD_FOLDER'], app.config['PROCESSED_FOLDER'], 'logs']:
    Path(folder).mkdir(parents=True, exist_ok=True)

# Initialize services with logging
logger.info("🔧 Initializing services...")
doc_processor = DocumentProcessor()
logger.info("   ✅ DocumentProcessor initialized")
ai_service = AIService()
logger.info("   ✅ AIService initialized")
placeholder_detector = PlaceholderDetector()
logger.info("   ✅ PlaceholderDetector initialized")
logger.info("   🔍 Checking session manager...")
# Force session manager initialization logging by accessing it
logger.info(f"   Redis Status: {'✅ Connected' if session_manager.use_redis else '❌ Using in-memory fallback'}")
if not session_manager.use_redis:
    logger.warning("   ⚠️  Redis is NOT connected - sessions will not persist across restarts!")
    logger.warning("   💡 Solution: Verify REDIS_URL is set in Render environment variables")
logger.info("=" * 60)

# Initialize Firebase (for auth)
logger.info("🔐 Initializing Firebase...")
from services.firebase_auth import initialize_firebase
initialize_firebase()
logger.info("=" * 60)

# Allowed file extensions for upload
ALLOWED_EXTENSIONS = {'docx', 'doc'}

# Session management is now handled by Redis via session_manager
# (falls back to in-memory if Redis unavailable)


def allowed_file(filename: str) -> bool:
    """
    Check if the uploaded file has an allowed extension.
    
    Args:
        filename (str): Name of the file to check
        
    Returns:
        bool: True if file extension is allowed, False otherwise
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Session management functions - now use Redis via session_manager
def get_session_data(session_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve session data using Redis session manager"""
    return session_manager.get_session(session_id)


def save_session_data(session_id: str, data: Dict[str, Any], user_id: Optional[str] = None) -> None:
    """Save session data using Redis session manager"""
    session_manager.save_session(session_id, data, user_id=user_id)


@app.route('/')
def index():
    """
    Root endpoint - returns API information.
    """
    logger.info(f"📥 Root endpoint hit from: {request.headers.get('Origin', 'Direct')}")
    return jsonify({
        'name': 'Legal Document Automation API',
        'version': '1.0.0',
        'status': 'operational',
        'backend_url': request.url_root,
        'endpoints': [
            '/api/upload',
            '/api/chat',
            '/api/preview',
            '/api/complete',
            '/api/download/<filename>',
            '/api/reset',
            '/api/health',
            '/api/groq/stream',
            '/api/groq/document-stream'
        ]
    })


@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for monitoring.
    Used by deployment platforms to verify the service is running.
    
    Returns:
        JSON response with service status
    """
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'Legal Document Automation Platform',
        'version': '1.0.0',
        'uptime': 'operational'
    })


@app.route('/api/upload', methods=['POST'])
def upload_document():
    logger.info("=" * 60)
    logger.info("📤 DOCUMENT UPLOAD REQUEST RECEIVED")
    logger.info("=" * 60)
    logger.info(f"   Request origin: {request.headers.get('Origin', 'Unknown')}")
    logger.info(f"   Content-Type: {request.headers.get('Content-Type', 'Unknown')}")
    logger.info(f"   Has file: {'document' in request.files}")
    """
    Handle document upload and initial processing.
    
    This endpoint:
    1. Validates the uploaded file
    2. Saves it to the upload directory
    3. Processes the document to extract content
    4. Detects placeholders
    5. Initializes a conversation session
    
    Returns:
        JSON response with session information and detected placeholders
    """
    try:
        # Validate file presence in request
        if 'document' not in request.files:
            logger.warning("Upload attempt with no document provided")
            return jsonify({
                'error': 'No document provided',
                'message': 'Please select a file to upload'
            }), 400
        
        file = request.files['document']
        
        # Validate file selection
        if file.filename == '':
            logger.warning("Upload attempt with empty filename")
            return jsonify({
                'error': 'No file selected',
                'message': 'Please select a valid document file'
            }), 400
        
        # Validate file type
        if not allowed_file(file.filename):
            logger.warning(f"Upload attempt with invalid file type: {file.filename}")
            return jsonify({
                'error': 'Invalid file format',
                'message': 'Please upload a .docx file. Other formats are not supported yet.'
            }), 400
        
        # Generate unique session ID
        session_id = str(uuid.uuid4())
        logger.info(f"Created new session: {session_id}")
        
        # Secure the filename and create unique path
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{session_id}_{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        # Save the uploaded file
        file.save(filepath)
        logger.info(f"Saved uploaded file: {unique_filename}")
        
        # Process document to extract content and structure
        logger.info(f"Processing document: {unique_filename}")
        doc_content = doc_processor.parse_document(filepath)
        
        if not doc_content:
            logger.error(f"Failed to parse document: {unique_filename}")
            return jsonify({
                'error': 'Document processing failed',
                'message': 'Unable to read the document. Please ensure it\'s a valid .docx file.'
            }), 500
        
        # Detect placeholders in the document
        placeholders = placeholder_detector.detect_placeholders(doc_content)
        logger.info(f"Detected {len(placeholders)} placeholders in document")
        
        # Initialize AI conversation context
        ai_context = ai_service.initialize_conversation(doc_content, placeholders)
        
        # Store session data
        now = datetime.now().isoformat()
        session_data = {
            'session_id': session_id,
            'filepath': filepath,
            'filename': filename,
            'content': doc_content,
            'placeholders': placeholders,
            'filled_values': {},
            'current_placeholder_index': 0,
            'ai_context': ai_context,
            'conversation_history': [],
            'created_at': now,
            'last_accessed_at': now,  # Track last access to prevent premature expiration
            'status': 'active'
        }
        
        # Get user_id from token if available
        user_id = None
        token = get_token_from_request(request)
        if token:
            user_info = verify_token(token)
            if user_info:
                user_id = user_info['uid']
                logger.info(f"Session linked to user: {user_id}")
        
        # Save session (this will also create history entry via session_manager)
        logger.info(f"💾 Saving session data for: {session_id[:8]}...")
        save_session_data(session_id, session_data, user_id=user_id)
        logger.info(f"✅ Session saved. Verifying...")
        
        # Verify session was saved
        verify_session = get_session_data(session_id)
        if verify_session:
            logger.info(f"✅ Session verified in storage: {session_id[:8]}...")
        else:
            logger.error(f"❌ CRITICAL: Session was NOT saved properly: {session_id[:8]}...")
        
        # Explicitly add session_created history entry
        session_manager.add_history(session_id, 'session_created', {
            'filename': filename,
            'placeholders_count': len(placeholders),
            'session_id': session_id,
            'user_id': user_id
        })
        
        # Prepare response
        response_data = {
            'success': True,
            'session_id': session_id,
            'filename': filename,
            'placeholders_count': len(placeholders),
            'placeholders': placeholders,
            'message': f'Document uploaded successfully. Found {len(placeholders)} placeholder{"s" if len(placeholders) != 1 else ""} to fill.',
            'initial_message': ai_service.get_greeting_message(placeholders)
        }
        
        logger.info(f"📤 Upload response prepared for session {session_id[:8]}... with {len(placeholders)} placeholders")
        return jsonify(response_data), 200
        
    except RequestEntityTooLarge:
        logger.error("File too large uploaded")
        return jsonify({
            'error': 'File too large',
            'message': f'File size exceeds the maximum limit of {app.config["MAX_CONTENT_LENGTH"] / (1024*1024):.1f}MB'
        }), 413
        
    except Exception as e:
        logger.error(f"Error processing upload: {str(e)}")
        return jsonify({
            'error': 'Processing error',
            'message': 'An unexpected error occurred while processing your document. Please try again.'
        }), 500


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Handle conversational interactions for filling placeholders.
    
    This endpoint:
    1. Processes user messages
    2. Validates inputs based on placeholder type
    3. Updates filled values
    4. Generates AI responses for next placeholder
    
    Returns:
        JSON response with AI message and progress information
    """
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id')
        
        if not session_id:
            logger.warning("Chat request without session_id")
            return jsonify({
                'error': 'No session found',
                'message': 'Please upload a document first to start a conversation.',
                'session_expired': False,
                'code': 'NO_SESSION'
            }), 400
        
        # Retrieve session data with better error handling
        session_data = get_session_data(session_id)
        if not session_data:
            # Try to get more info for debugging
            all_sessions = session_manager.get_all_sessions(limit=5)
            active_session_ids = [s['session_id'] for s in all_sessions][:5]
            logger.warning(
                f"Chat request with invalid or expired session_id: {session_id[:8]}... "
                f"Active sessions: {len(all_sessions)}. First 5: {[s[:8] + '...' for s in active_session_ids]}"
            )
            return jsonify({
                'error': 'Session expired',
                'message': 'Your session has expired. Please upload the document again.',
                'session_expired': True,
                'code': 'SESSION_EXPIRED'
            }), 400
        
        # Extract session information
        placeholders = session_data['placeholders']
        filled_values = session_data['filled_values']
        current_index = session_data['current_placeholder_index']
        ai_context = session_data['ai_context']
        conversation_history = session_data.get('conversation_history', [])
        
        # Add user message to history
        conversation_history.append({
            'role': 'user',
            'content': user_message,
            'timestamp': datetime.now().isoformat()
        })
        
        # Process user message with AI
        response = ai_service.process_message(
            user_message=user_message,
            placeholders=placeholders,
            filled_values=filled_values,
            current_index=current_index,
            ai_context=ai_context
        )
        
        # Update session based on response
        if response.get('placeholder_filled'):
            placeholder_key = response['placeholder_key']
            filled_values[placeholder_key] = response['value']
            session_data['filled_values'] = filled_values
            
            logger.info(f"Filled placeholder {placeholder_key} with value: {response['value'][:50]}...")
            
            # Handle auto-fills (e.g., duplicate fields like "Disclosing Party Address")
            if 'auto_fills' in response:
                for auto_fill in response['auto_fills']:
                    filled_values[auto_fill['key']] = auto_fill['value']
                    session_data['filled_values'] = filled_values
                    auto_fill_name = auto_fill.get('name', 'unknown field')
                    logger.info(
                        f"Auto-filled '{auto_fill_name}' (id: {auto_fill['key']}) "
                        f"with value: {auto_fill['value'][:50]}..."
                    )
            
            # Update current index using next_index from response (accounts for auto-fills)
            # This ensures we skip auto-filled fields and move to the correct next unfilled field
            if 'next_index' in response and response['next_index'] is not None:
                session_data['current_placeholder_index'] = response['next_index']
                logger.debug(f"Updated current_placeholder_index to {response['next_index']} based on response")
            else:
                # Fallback: If no next_index provided, use the next sequential index
                # This should rarely happen, but provides safety
                session_data['current_placeholder_index'] = current_index + 1
                logger.warning(
                    f"No next_index in response, using fallback: {current_index + 1}. "
                    f"Total filled: {len(filled_values)}, Total placeholders: {len(placeholders)}"
                )
        
        # Add AI response to history
        conversation_history.append({
            'role': 'assistant',
            'content': response['message'],
            'timestamp': datetime.now().isoformat()
        })
        
        session_data['conversation_history'] = conversation_history
        save_session_data(session_id, session_data)
        
        # Check if all placeholders are filled
        all_filled = len(filled_values) == len(placeholders)
        
        # Determine preview index: use next_index from response if available, otherwise use session index
        # If next_index is None, all fields are filled
        preview_index = None
        if response.get('next_index') is not None:
            preview_index = response['next_index']
        elif not all_filled:
            # Fallback to session index if not all filled
            preview_index = session_data['current_placeholder_index']
            if preview_index >= len(placeholders):
                preview_index = None  # Safety check
        
        # Generate fresh preview HTML to return with response
        preview_html = doc_processor.generate_preview(
            content=session_data['content'],
            placeholders=placeholders,
            filled_values=filled_values,
            current_index=preview_index
        )
        
        # Prepare response
        response_data = {
            'response': response['message'],
            'placeholder_filled': response.get('placeholder_filled', False),
            'current_progress': session_data['current_placeholder_index'],
            'total_placeholders': len(placeholders),
            'progress_percentage': round((len(filled_values) / len(placeholders) * 100), 1) if placeholders else 0,
            'all_filled': all_filled,
            'filled_values': filled_values,
            'current_placeholder': placeholders[preview_index] if preview_index is not None and preview_index < len(placeholders) else None,
            'preview': preview_html  # NEW: fresh preview with each response
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({
            'error': 'Chat processing error',
            'message': 'An error occurred while processing your message. Please try again.'
        }), 500


@app.route('/api/edit', methods=['POST'])
def edit_field():
    """
    Edit a previously filled field value.
    
    This endpoint allows users to go back and edit any filled field.
    
    Returns:
        JSON response with updated preview and confirmation
    """
    try:
        data = request.json
        session_id = data.get('session_id')
        field_key = data.get('field_key')
        new_value = data.get('value', '').strip()
        
        if not session_id:
            return jsonify({
                'error': 'No session found',
                'message': 'Please upload a document first.'
            }), 400
        
        if not field_key:
            return jsonify({
                'error': 'No field specified',
                'message': 'Please specify which field to edit.'
            }), 400
        
        # Retrieve session data
        session_data = get_session_data(session_id)
        if not session_data:
            return jsonify({
                'error': 'Session expired',
                'message': 'Your session has expired. Please upload the document again.'
            }), 400
        
        placeholders = session_data['placeholders']
        filled_values = session_data['filled_values']
        
        # Find the placeholder by ID or key (support both)
        placeholder = None
        placeholder_id = None
        
        for p in placeholders:
            if p.get('id') == field_key or p['key'] == field_key:
                placeholder = p
                placeholder_id = p.get('id', p['key'])
                break
        
        if not placeholder:
            return jsonify({
                'error': 'Field not found',
                'message': 'The specified field does not exist.'
            }), 400
        
        # Validate the new value
        validation_result = ai_service._validate_placeholder_value(new_value, placeholder)
        
        if not validation_result['valid']:
            return jsonify({
                'error': 'Invalid value',
                'message': validation_result['error_message']
            }), 400
        
        # Update the value (store by both ID and key for compatibility)
        filled_values[placeholder_id] = validation_result['processed_value']
        if placeholder_id != field_key:
            filled_values[field_key] = validation_result['processed_value']
        session_data['filled_values'] = filled_values
        
        # Handle auto-fills for duplicate fields (same as in chat endpoint)
        current_name = placeholder['name']
        auto_filled = []
        for ph in placeholders:
            if (ph.get('id', ph['key']) != placeholder_id and 
                ph['name'] == current_name):
                ph_id = ph.get('id', ph['key'])
                filled_values[ph_id] = validation_result['processed_value']
                auto_filled.append(ph_id)
        
        if auto_filled:
            logger.info(f"Auto-filled {len(auto_filled)} duplicate fields when editing '{current_name}'")
        
        # Update current index to this field if needed (allow editing any field)
        field_index = next((i for i, p in enumerate(placeholders) if p['key'] == field_key), None)
        if field_index is not None:
            session_data['current_placeholder_index'] = field_index
        
        save_session_data(session_id, session_data)
        
        # Generate updated preview
        current_index = len(filled_values) if len(filled_values) < len(placeholders) else None
        preview_html = doc_processor.generate_preview(
            content=session_data['content'],
            placeholders=placeholders,
            filled_values=filled_values,
            current_index=current_index
        )
        
        # Prepare response
        response_data = {
            'success': True,
            'message': f'Field "{placeholder.get("name", "Field")}" updated successfully.',
            'preview': preview_html,
            'filled_count': len(filled_values),
            'total_count': len(placeholders),
            'progress_percentage': round(
                (len(filled_values) / len(placeholders) * 100), 1
            ) if placeholders else 0,
            'filled_values': filled_values,
            'current_index': current_index
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        logger.error(f"Error editing field: {str(e)}")
        return jsonify({
            'error': 'Edit processing error',
            'message': 'An error occurred while updating the field. Please try again.'
        }), 500


@app.route('/api/session/health', methods=['GET'])
def session_health():
    """
    Check if a session is still valid and active.
    
    Returns:
        JSON response with session status
    """
    try:
        session_id = request.args.get('session_id')
        
        if not session_id:
            return jsonify({
                'valid': False,
                'error': 'No session ID provided',
                'message': 'Session ID is required.'
            }), 400
        
        session_data = get_session_data(session_id)
        
        if session_data:
            return jsonify({
                'valid': True,
                'session_id': session_id,
                'has_document': 'content' in session_data,
                'placeholders_count': len(session_data.get('placeholders', [])),
                'filled_count': len(session_data.get('filled_values', {})),
                'last_accessed': session_data.get('last_accessed_at')
            }), 200
        else:
            return jsonify({
                'valid': False,
                'error': 'Session not found',
                'message': 'Session expired or invalid.',
                'session_expired': True
            }), 404
            
    except Exception as e:
        logger.error(f"Error checking session health: {str(e)}")
        return jsonify({
            'valid': False,
            'error': 'Health check failed',
            'message': 'An error occurred while checking session status.'
        }), 500


@app.route('/api/sessions', methods=['GET'])
def get_all_sessions():
    """
    Get all active sessions with metadata (filtered by authenticated user).
    
    Query params:
        limit: Maximum number of sessions to return (default: 100)
    
    Returns:
        JSON response with list of sessions
    """
    try:
        limit = int(request.args.get('limit', 100))
        
        # Get user_id from token if available
        user_id = None
        token = get_token_from_request(request)
        if token:
            user_info = verify_token(token)
            if user_info:
                user_id = user_info['uid']
        
        sessions = session_manager.get_all_sessions(limit=limit, user_id=user_id)
        
        return jsonify({
            'success': True,
            'sessions': sessions,
            'count': len(sessions),
            'user_id': user_id
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting sessions: {str(e)}")
        return jsonify({
            'error': 'Failed to retrieve sessions',
            'message': 'An error occurred while fetching sessions.'
        }), 500


@app.route('/api/sessions/history', methods=['GET'])
def get_session_history():
    """
    Get history for a specific session.
    
    Query params:
        session_id: Session identifier (required)
        limit: Maximum number of history entries (default: 50)
    
    Returns:
        JSON response with session history
    """
    try:
        session_id = request.args.get('session_id')
        limit = int(request.args.get('limit', 50))
        
        if not session_id:
            return jsonify({
                'error': 'No session ID provided',
                'message': 'Session ID is required.'
            }), 400
        
        history = session_manager.get_session_history(session_id, limit=limit)
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'history': history,
            'count': len(history)
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting session history: {str(e)}")
        return jsonify({
            'error': 'Failed to retrieve history',
            'message': 'An error occurred while fetching session history.'
        }), 500


@app.route('/api/sessions/stats', methods=['GET'])
def get_session_stats():
    """
    Get overall session statistics.
    
    Returns:
        JSON response with session statistics
    """
    try:
        stats = session_manager.get_session_stats()
        
        return jsonify({
            'success': True,
            'stats': stats
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting session stats: {str(e)}")
        return jsonify({
            'error': 'Failed to retrieve stats',
            'message': 'An error occurred while fetching statistics.'
        }), 500


@app.route('/api/fill', methods=['POST'])
def fill_field_directly():
    logger.info("=" * 60)
    logger.info("✏️  FILL FIELD REQUEST RECEIVED")
    logger.info("=" * 60)
    data = request.json
    session_id = data.get('session_id') if data else None
    logger.info(f"   Session ID from request: {session_id[:8] if session_id else 'MISSING'}...")
    logger.info(f"   Request origin: {request.headers.get('Origin', 'Unknown')}")
    """
    Fill a field directly (for inline editing in document preview).
    Works for both filled and unfilled fields.
    
    Returns:
        JSON response with updated preview
    """
    try:
        data = request.json
        session_id = data.get('session_id')
        field_key = data.get('field_key')  # Can be ID or key
        value = data.get('value', '').strip()
        
        if not session_id:
            return jsonify({
                'error': 'No session found',
                'message': 'Session ID is required.'
            }), 400
        
        if not field_key:
            return jsonify({
                'error': 'No field specified',
                'message': 'Field identifier is required.'
            }), 400
        
        # Retrieve session data
        session_data = get_session_data(session_id)
        if not session_data:
            # Log for debugging
            logger.warning(
                f"Fill field request with invalid session: {session_id[:8]}... "
                f"Redis available: {session_manager.use_redis}"
            )
            return jsonify({
                'error': 'Session expired',
                'message': 'Your session has expired. Please upload the document again.',
                'session_expired': True
            }), 400
        
        placeholders = session_data['placeholders']
        filled_values = session_data['filled_values']
        
        # Find placeholder by ID or key
        placeholder = None
        placeholder_id = None
        
        for p in placeholders:
            if p.get('id') == field_key or p['key'] == field_key:
                placeholder = p
                placeholder_id = p.get('id', p['key'])
                break
        
        if not placeholder:
            return jsonify({
                'error': 'Field not found',
                'message': 'The specified field does not exist.'
            }), 400
        
        # Validate value
        validation_result = ai_service._validate_placeholder_value(value, placeholder)
        
        if not validation_result['valid']:
            return jsonify({
                'error': 'Invalid value',
                'message': validation_result['error_message']
            }), 400
        
        # Update value
        processed_value = validation_result['processed_value']
        filled_values[placeholder_id] = processed_value
        
        # Auto-fill duplicate fields
        current_name = placeholder['name']
        auto_filled = []
        for ph in placeholders:
            if (ph.get('id', ph['key']) != placeholder_id and 
                ph['name'] == current_name):
                ph_id = ph.get('id', ph['key'])
                if ph_id not in filled_values:
                    filled_values[ph_id] = processed_value
                    auto_filled.append(ph['name'])
        
        session_data['filled_values'] = filled_values
        save_session_data(session_id, session_data)
        
        # Calculate next unfilled index
        all_filled_keys = set(filled_values.keys())
        next_index = None
        for i, ph in enumerate(placeholders):
            ph_id = ph.get('id', ph['key'])
            if ph_id not in all_filled_keys and ph['key'] not in all_filled_keys:
                next_index = i
                break
        
        # Generate preview
        preview_html = doc_processor.generate_preview(
            content=session_data['content'],
            placeholders=placeholders,
            filled_values=filled_values,
            current_index=next_index
        )
        
        response_data = {
            'success': True,
            'message': f'Field "{current_name}" filled successfully.' + 
                      (f' Auto-filled {len(auto_filled)} duplicate field(s).' if auto_filled else ''),
            'preview': preview_html,
            'filled_count': len(filled_values),
            'total_count': len(placeholders),
            'progress_percentage': round((len(filled_values) / len(placeholders) * 100), 1) if placeholders else 0,
            'filled_values': filled_values,
            'next_index': next_index,
            'auto_filled': auto_filled
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        logger.error(f"Error filling field directly: {str(e)}")
        return jsonify({
            'error': 'Fill processing error',
            'message': 'An error occurred while filling the field. Please try again.'
        }), 500


@app.route('/api/preview', methods=['GET'])
def preview_document():
    """
    Generate and return a preview of the document with current filled values.
    
    Returns:
        JSON response with HTML preview of the document
    """
    try:
        session_id = request.args.get('session_id')
        
        if not session_id:
            return jsonify({
                'error': 'No session specified',
                'message': 'Session ID is required for preview.'
            }), 400
        
        # Retrieve session data
        session_data = get_session_data(session_id)
        if not session_data:
            return jsonify({
                'error': 'Session not found',
                'message': 'Session expired or invalid. Please upload the document again.'
            }), 400
        
        # Get current field index (for highlighting)
        current_index = session_data.get('current_placeholder_index', None)
        filled_count = len(session_data['filled_values'])
        
        # Current index should be based on filled count (next field to fill)
        if current_index is None:
            current_index = filled_count if filled_count < len(session_data['placeholders']) else None
        
        # Generate preview with current field highlighting
        preview_html = doc_processor.generate_preview(
            content=session_data['content'],
            placeholders=session_data['placeholders'],
            filled_values=session_data['filled_values'],
            current_index=current_index
        )
        
        # Prepare response
        response_data = {
            'preview': preview_html,
            'filled_count': filled_count,
            'total_count': len(session_data['placeholders']),
            'progress_percentage': round(
                (filled_count / len(session_data['placeholders']) * 100), 1
            ) if session_data['placeholders'] else 0,
            'placeholders': session_data['placeholders'],
            'filled_values': session_data['filled_values'],
            'current_index': current_index
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        logger.error(f"Error generating preview: {str(e)}")
        return jsonify({
            'error': 'Preview generation error',
            'message': 'Unable to generate document preview. Please try again.'
        }), 500


@app.route('/api/complete', methods=['POST'])
def complete_document():
    """
    Generate the final document with all filled values.
    
    This endpoint:
    1. Validates all placeholders are filled
    2. Generates the final document
    3. Saves it to the processed folder
    4. Returns download information
    
    Returns:
        JSON response with download URL
    """
    try:
        data = request.json
        session_id = data.get('session_id')
        
        if not session_id:
            return jsonify({
                'error': 'No session specified',
                'message': 'Session ID is required to complete the document.'
            }), 400
        
        # Retrieve session data
        session_data = get_session_data(session_id)
        if not session_data:
            return jsonify({
                'error': 'Session not found',
                'message': 'Session expired or invalid. Please upload the document again.'
            }), 400
        
        # Validate all placeholders are filled
        placeholders = session_data['placeholders']
        filled_values = session_data['filled_values']
        
        if len(filled_values) < len(placeholders):
            unfilled = [p for p in placeholders if p['key'] not in filled_values]
            unfilled_names = [p['name'] for p in unfilled[:5]]  # Show first 5 unfilled
            
            return jsonify({
                'error': 'Incomplete document',
                'message': f'Please fill all placeholders before downloading. Still missing: {", ".join(unfilled_names)}{"..." if len(unfilled) > 5 else ""}',
                'unfilled_count': len(unfilled),
                'unfilled_placeholders': unfilled
            }), 400
        
        # Generate output filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        original_name = session_data['filename'].rsplit('.', 1)[0]
        output_filename = f"completed_{original_name}_{timestamp}.docx"
        output_path = os.path.join(app.config['PROCESSED_FOLDER'], output_filename)
        
        # Generate final document
        logger.info(f"Generating final document for session {session_id}")
        
        # 🔍 DEBUG: Log all placeholders and their values
        logger.info("="*80)
        logger.info("DOCUMENT COMPLETION DEBUG")
        logger.info("="*80)
        logger.info(f"Total placeholders: {len(placeholders)}")
        
        # Check for dollar placeholders specifically
        dollar_placeholders = [p for p in placeholders if '$' in p.get('original', '')]
        logger.info(f"\nDollar placeholders ({len(dollar_placeholders)}):")
        for p in dollar_placeholders:
            logger.info(f"  {p['name']}")
            logger.info(f"    Key: {p['key']}")
            logger.info(f"    Location: {p['location']} ({p['location_type']})")
            logger.info(f"    Original: {p['original']}")
            logger.info(f"    Value in filled_values: {filled_values.get(p['key'], 'NOT FOUND')}")
        
        logger.info("\nAll filled values:")
        for key, value in filled_values.items():
            logger.info(f"  {key} = {value}")
        logger.info("="*80)
        
        success = doc_processor.generate_final_document(
            template_path=session_data['filepath'],
            output_path=output_path,
            placeholders=placeholders,
            filled_values=filled_values
        )
        
        if not success:
            logger.error(f"Failed to generate final document for session {session_id}")
            return jsonify({
                'error': 'Document generation failed',
                'message': 'Unable to generate the final document. Please try again.'
            }), 500
        
        # Update session data
        session_data['completed_document'] = output_path
        session_data['completed_at'] = datetime.now().isoformat()
        session_data['status'] = 'completed'
        save_session_data(session_id, session_data)
        
        logger.info(f"Document completed successfully: {output_filename}")
        
        return jsonify({
            'success': True,
            'download_url': f'/api/download/{output_filename}',
            'filename': output_filename,
            'message': 'Document completed successfully! Click the download button to save your file.'
        }), 200
        
    except Exception as e:
        logger.error(f"Error completing document: {str(e)}")
        return jsonify({
            'error': 'Completion error',
            'message': 'An error occurred while generating the final document. Please try again.'
        }), 500


@app.route('/api/download/<filename>')
def download_document(filename):
    """
    Download the completed document.
    
    Args:
        filename (str): Name of the file to download
        
    Returns:
        File download response
    """
    try:
        # Secure the filename
        filename = secure_filename(filename)
        filepath = os.path.join(app.config['PROCESSED_FOLDER'], filename)
        
        # Check if file exists
        if not os.path.exists(filepath):
            logger.warning(f"Download attempt for non-existent file: {filename}")
            return jsonify({
                'error': 'File not found',
                'message': 'The requested file could not be found. It may have expired.'
            }), 404
        
        # Send file
        logger.info(f"Downloading file: {filename}")
        return send_file(
            filepath,
            as_attachment=True,
            download_name=filename,
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        
    except Exception as e:
        logger.error(f"Error downloading document: {str(e)}")
        return jsonify({
            'error': 'Download error',
            'message': 'Unable to download the file. Please try again.'
        }), 500


@app.route('/api/reset', methods=['POST'])
def reset_session():
    """
    Reset the current session and clean up resources.
    
    Returns:
        JSON response confirming reset
    """
    try:
        data = request.json
        session_id = data.get('session_id')
        
        if session_id:
            # Get session data first
            session_data = get_session_data(session_id)
            if session_data:
                # Clean up uploaded file
                if 'filepath' in session_data:
                    try:
                        os.remove(session_data['filepath'])
                        logger.info(f"Cleaned up file for session {session_id}")
                    except:
                        pass
                
                # Delete session from Redis
                session_manager.delete_session(session_id)
                logger.info(f"Reset session: {session_id}")
        
        return jsonify({
            'success': True,
            'message': 'Session reset successfully. You can now upload a new document.'
        }), 200
        
    except Exception as e:
        logger.error(f"Error resetting session: {str(e)}")
        return jsonify({
            'error': 'Reset error',
            'message': 'Unable to reset session. Please refresh the page.'
        }), 500


@app.errorhandler(413)
def request_entity_too_large(error):
    """
    Handle file too large errors.
    
    Returns:
        JSON error response for oversized files
    """
    return jsonify({
        'error': 'File too large',
        'message': f'The uploaded file exceeds the maximum size limit of {app.config["MAX_CONTENT_LENGTH"] / (1024*1024):.1f}MB. Please upload a smaller file.'
    }), 413


@app.errorhandler(500)
def internal_server_error(error):
    """
    Handle internal server errors.
    
    Returns:
        JSON error response for server errors
    """
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred. Our team has been notified. Please try again later.'
    }), 500


@app.before_request
def before_request():
    """
    Execute before each request.
    Used for request logging and validation.
    """
    logger.info(f"{request.method} {request.path} from {request.remote_addr}")


@app.after_request
def after_request(response):
    """
    Execute after each request.
    Add security headers and log response.
    
    Args:
        response: Flask response object
        
    Returns:
        Modified response with additional headers
    """
    # CORS headers are handled by flask-cors extension
    # Flask-CORS automatically sets the correct headers based on the requesting origin
    
    # Add security headers
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    
    # Only add HSTS in production
    if os.environ.get('FLASK_ENV') != 'development':
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    
    return response


def _run_app():
    """
    Run the Flask application.
    In production, use Gunicorn or similar WSGI server.
    """
    port = int(os.environ.get('PORT', 5001))  # Default to 5001 to avoid macOS AirPlay conflict
    debug = os.environ.get('FLASK_ENV', 'development') == 'development'

    logger.info(f"Starting Legal Document Automation Platform on port {port}")
    logger.info(f"Debug mode: {debug}")
    logger.info(f"CORS enabled for: http://localhost:3000, http://localhost:3001")

    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )

"""
Additional AI (Groq) endpoints
------------------------------
Provides a lightweight streaming proxy to Groq as requested, using the
exact streaming pattern the user provided. Returns plain text chunks.
"""

try:
    from groq import Groq  # type: ignore
    _groq_import_ok = True
except Exception:
    _groq_import_ok = False


@app.route('/api/groq/stream', methods=['POST'])
def groq_stream():
    """
    Stream a generic AI response from Groq to the client.

    Request JSON:
      - prompt: string (required)
      - model: string (optional; default: openai/gpt-oss-120b)

    Response: text/plain streamed chunks containing the model output.
    """
    if not _groq_import_ok:
        return jsonify({
            'error': 'Groq unavailable',
            'message': 'groq package not installed on server'
        }), 500

    try:
        body = request.get_json(silent=True) or {}
        prompt = (body.get('prompt') or '').strip()
        model = body.get('model') or os.environ.get('GROQ_MODEL', 'openai/gpt-oss-120b')

        if not prompt:
            return jsonify({'error': 'Missing prompt', 'message': 'Provide a non-empty prompt'}), 400

        # Optional auth: accept Firebase token but do not hard-fail if absent
        token = get_token_from_request(request)
        if token:
            _ = verify_token(token)  # Best-effort verification

        client = Groq(api_key=os.environ.get('GROQ_API_KEY'))

        def generate():
            completion = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=1,
                max_completion_tokens=8192,
                top_p=1,
                reasoning_effort="medium",
                stream=True,
                stop=None,
            )

            for chunk in completion:
                try:
                    text = chunk.choices[0].delta.content or ""
                except Exception:
                    text = ""
                if text:
                    yield text

        resp = Response(stream_with_context(generate()), mimetype='text/plain')
        # Extra CORS safety for streaming responses
        origin = request.headers.get('Origin')
        if origin in allowed_origins:
            resp.headers['Access-Control-Allow-Origin'] = origin
            resp.headers['Access-Control-Allow-Credentials'] = 'true'
        return resp

    except Exception as e:
        logger.error(f"Error in Groq stream: {e}")
        return jsonify({'error': 'Groq stream failed', 'message': str(e)}), 500


@app.route('/api/groq/document-stream', methods=['POST'])
def groq_document_stream():
    """
    Stream a document-aware AI response from Groq to the client.
    
    Request JSON:
      - prompt: string (required) - User's question
      - document_context: dict (optional) - Contains document information:
          - sessionId: string
          - filename: string
          - placeholders: list of placeholder objects
          - filledValues: dict of filled values
          - previewHtml: string (HTML preview)
      - model: string (optional)
    
    Response: text/plain streamed chunks containing the model output.
    """
    if not _groq_import_ok:
        return jsonify({
            'error': 'Groq unavailable',
            'message': 'groq package not installed on server'
        }), 500

    try:
        body = request.get_json(silent=True) or {}
        user_prompt = (body.get('prompt') or '').strip()
        doc_context = body.get('document_context') or {}
        model = body.get('model') or os.environ.get('GROQ_MODEL', 'openai/gpt-oss-120b')

        if not user_prompt:
            return jsonify({'error': 'Missing prompt', 'message': 'Provide a non-empty prompt'}), 400

        # Optional auth
        token = get_token_from_request(request)
        if token:
            _ = verify_token(token)

        # Build context-aware prompt
        context_parts = []
        
        if doc_context.get('filename'):
            context_parts.append(f"Document: {doc_context['filename']}")
        
        if doc_context.get('placeholders'):
            placeholders = doc_context['placeholders']
            total_fields = len(placeholders)
            context_parts.append(f"Total fields in document: {total_fields}")
            
            # Show some placeholder names
            field_names = [p.get('name', p.get('key', '')) for p in placeholders[:10]]
            if field_names:
                context_parts.append(f"Fields include: {', '.join(field_names)}")
        
        if doc_context.get('filledValues'):
            filled_values = doc_context['filledValues']
            filled_count = len(filled_values)
            context_parts.append(f"Fields completed: {filled_count}")
            
            # Show some filled values (for context)
            filled_items = list(filled_values.items())[:5]
            if filled_items:
                filled_summary = [f"{k}: {v}" for k, v in filled_items]
                context_parts.append(f"Some filled values: {'; '.join(filled_summary)}")
        
        # Build the enhanced prompt in a conversational way
        if context_parts:
            system_context = "I'm analyzing a legal document for the user. Here's what I know about it:\n\n"
            system_context += "\n".join(context_parts)
            system_context += "\n\nThe user wants to know: " + user_prompt
            system_context += "\n\nI should explain this in a clear, conversational way using natural paragraphs. No tables or complex formatting - just friendly, easy-to-understand explanations with examples where helpful."
            
            full_prompt = system_context
        else:
            full_prompt = user_prompt

        client = Groq(api_key=os.environ.get('GROQ_API_KEY'))

        def generate():
            completion = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": """You are a helpful legal AI assistant. You help users understand legal documents, explain terms, and provide guidance on legal matters.

IMPORTANT FORMATTING RULES:
- Write in natural, conversational paragraphs
- DO NOT use tables, markdown tables, or structured lists with pipes (|)
- Use simple bullet points (•) when listing items, never complex tables
- Write as if explaining to a friend over coffee
- Break complex topics into short, easy-to-read paragraphs
- Use examples and analogies to explain difficult concepts
- Keep responses friendly, clear, and professional
- Format for easy reading in a chat interface

Be accurate and helpful, but always prioritize readability and natural conversation flow."""},
                    {"role": "user", "content": full_prompt}
                ],
                temperature=0.7,
                max_completion_tokens=8192,
                top_p=1,
                stream=True,
                stop=None,
            )

            for chunk in completion:
                try:
                    text = chunk.choices[0].delta.content or ""
                except Exception:
                    text = ""
                if text:
                    yield text

        resp = Response(stream_with_context(generate()), mimetype='text/plain')
        # Extra CORS safety for streaming responses
        origin = request.headers.get('Origin')
        if origin in allowed_origins:
            resp.headers['Access-Control-Allow-Origin'] = origin
            resp.headers['Access-Control-Allow-Credentials'] = 'true'
        return resp

    except Exception as e:
        logger.error(f"Error in Groq document stream: {e}")
        return jsonify({'error': 'Groq document stream failed', 'message': str(e)}), 500


@app.route('/api/groq', methods=['POST'])
def groq_complete():
    """
    Non-streaming Groq completion (JSON). Used as a fallback when streaming
    is blocked by the environment. Returns { text }.
    """
    if not _groq_import_ok:
        return jsonify({'error': 'Groq unavailable', 'message': 'groq package not installed'}), 500
    try:
        body = request.get_json(silent=True) or {}
        prompt = (body.get('prompt') or '').strip()
        model = body.get('model') or os.environ.get('GROQ_MODEL', 'openai/gpt-oss-120b')
        if not prompt:
            return jsonify({'error': 'Missing prompt', 'message': 'Provide a non-empty prompt'}), 400

        token = get_token_from_request(request)
        if token:
            _ = verify_token(token)

        client = Groq(api_key=os.environ.get('GROQ_API_KEY'))

        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=1,
            max_completion_tokens=8192,
            top_p=1,
            reasoning_effort="medium",
            stream=False,
        )
        text = response.choices[0].message.content or ''
        return jsonify({ 'text': text })
    except Exception as e:
        logger.error(f"Error in Groq complete: {e}")
        return jsonify({'error': 'Groq request failed', 'message': str(e)}), 500


if __name__ == '__main__':
    _run_app()