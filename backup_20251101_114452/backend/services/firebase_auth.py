"""
Firebase Authentication Service
Handles user authentication and token verification for the backend
"""

import os
import firebase_admin
from firebase_admin import credentials, auth
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

# Initialize Firebase Admin SDK
_firebase_app = None


def initialize_firebase():
    """Initialize Firebase Admin SDK"""
    global _firebase_app
    
    if _firebase_app is not None:
        return _firebase_app
    
    # Get service account file path
    service_account_path = os.environ.get(
        'FIREBASE_SERVICE_ACCOUNT',
        os.path.join(os.path.dirname(__file__), '..', 'firebase-service-account.json')
    )
    
    if not os.path.exists(service_account_path):
        logger.warning("⚠️ Firebase service account file not found. Auth will be disabled.")
        logger.warning(f"   Expected path: {service_account_path}")
        logger.warning("   Set FIREBASE_SERVICE_ACCOUNT env var or place file in backend/ directory")
        return None
    
    try:
        cred = credentials.Certificate(service_account_path)
        _firebase_app = firebase_admin.initialize_app(cred)
        logger.info("✅ Firebase Admin initialized successfully")
        return _firebase_app
    except Exception as e:
        logger.error(f"❌ Failed to initialize Firebase: {e}")
        return None


def verify_token(id_token: str) -> Optional[Dict[str, Any]]:
    """
    Verify Firebase ID token and return decoded token.
    
    Args:
        id_token: Firebase ID token from client
        
    Returns:
        Decoded token with user info, or None if invalid
    """
    try:
        if _firebase_app is None:
            initialize_firebase()
        
        if _firebase_app is None:
            logger.warning("Firebase not initialized, cannot verify token")
            return None
        
        decoded_token = auth.verify_id_token(id_token)
        return {
            'uid': decoded_token['uid'],
            'email': decoded_token.get('email'),
            'name': decoded_token.get('name'),
            'picture': decoded_token.get('picture'),
        }
    except auth.InvalidIdTokenError:
        logger.warning("Invalid ID token provided")
        return None
    except auth.ExpiredIdTokenError:
        logger.warning("Expired ID token provided")
        return None
    except Exception as e:
        logger.error(f"Token verification failed: {e}")
        return None


def get_user_by_id(uid: str) -> Optional[Dict[str, Any]]:
    """Get user information by Firebase UID"""
    try:
        if _firebase_app is None:
            initialize_firebase()
        
        if _firebase_app is None:
            return None
        
        user = auth.get_user(uid)
        return {
            'uid': user.uid,
            'email': user.email,
            'name': user.display_name,
            'picture': user.photo_url,
        }
    except Exception as e:
        logger.error(f"Failed to get user: {e}")
        return None


def get_token_from_request(request) -> Optional[str]:
    """
    Extract Firebase token from request headers.
    
    Args:
        request: Flask request object
        
    Returns:
        Token string or None
    """
    auth_header = request.headers.get('Authorization')
    
    if not auth_header:
        return None
    
    if auth_header.startswith('Bearer '):
        return auth_header.split('Bearer ')[1]
    
    return None


# Initialize on import
initialize_firebase()

