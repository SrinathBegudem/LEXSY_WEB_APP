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
    """Initialize Firebase Admin SDK with detailed logging"""
    global _firebase_app
    
    if _firebase_app is not None:
        logger.info("✅ Firebase Admin already initialized")
        return _firebase_app
    
    logger.info("=" * 60)
    logger.info("🔍 FIREBASE INITIALIZATION")
    logger.info("=" * 60)
    
    # Get service account file path
    service_account_path = os.environ.get(
        'FIREBASE_SERVICE_ACCOUNT',
        os.path.join(os.path.dirname(__file__), '..', 'firebase-service-account.json')
    )
    
    logger.info(f"📋 Checking for Firebase service account file...")
    logger.info(f"   Expected path: {service_account_path}")
    logger.info(f"   Custom path env var: {os.environ.get('FIREBASE_SERVICE_ACCOUNT', 'NOT SET')}")
    
    if not os.path.exists(service_account_path):
        logger.warning("=" * 60)
        logger.warning("⚠️  FIREBASE SERVICE ACCOUNT FILE NOT FOUND")
        logger.warning("=" * 60)
        logger.warning(f"   Expected path: {service_account_path}")
        logger.warning("   🔧 Solutions:")
        logger.warning("      1. Upload firebase-service-account.json to Render Dashboard")
        logger.warning("         → Settings → Environment Files → Add File")
        logger.warning("      2. Or set FIREBASE_SERVICE_ACCOUNT env var with full path")
        logger.warning("   ⚠️  Firebase Authentication will be DISABLED")
        logger.warning("=" * 60)
        return None
    
    try:
        logger.info("   ✅ File found! Initializing Firebase Admin SDK...")
        cred = credentials.Certificate(service_account_path)
        _firebase_app = firebase_admin.initialize_app(cred)
        logger.info("=" * 60)
        logger.info("✅ FIREBASE ADMIN INITIALIZED SUCCESSFULLY")
        logger.info("=" * 60)
        return _firebase_app
    except Exception as e:
        logger.error("=" * 60)
        logger.error("❌ FIREBASE INITIALIZATION FAILED")
        logger.error("=" * 60)
        logger.error(f"   Error Type: {type(e).__name__}")
        logger.error(f"   Error Message: {str(e)}")
        logger.error("=" * 60)
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

