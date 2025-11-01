"""
Redis-based Session Manager with History Tracking
==================================================
Manages user sessions using Redis with comprehensive history logging.

Features:
- Session CRUD operations
- Session history tracking
- Automatic expiration
- Fallback to in-memory storage if Redis unavailable
- Session statistics and analytics
"""

import json
import logging
import redis
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# Redis configuration - support both REDIS_URL and individual settings
REDIS_URL = os.environ.get('REDIS_URL', None)
REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
REDIS_DB = int(os.environ.get('REDIS_DB', 0))
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', None)
SESSION_TIMEOUT_HOURS = int(os.environ.get('SESSION_TIMEOUT_HOURS', 168))  # 7 days

# Redis key prefixes
SESSION_PREFIX = "session:"
HISTORY_PREFIX = "history:"
STATS_PREFIX = "stats:"


class SessionManager:
    """Manages sessions using Redis with history tracking"""
    
    def __init__(self):
        self.redis_client = None
        self.use_redis = False
        self.fallback_store = {}  # In-memory fallback
        self._connect_redis()
    
    def _connect_redis(self):
        """Attempt to connect to Redis with detailed logging"""
        logger.info("=" * 60)
        logger.info("🔍 REDIS CONNECTION ATTEMPT")
        logger.info("=" * 60)
        
        # Log configuration
        if REDIS_URL:
            logger.info(f"📋 REDIS_URL is set (length: {len(REDIS_URL)} chars)")
            logger.info(f"   URL preview: {REDIS_URL[:20]}...{REDIS_URL[-10:] if len(REDIS_URL) > 30 else ''}")
        else:
            logger.info("📋 REDIS_URL is NOT set")
            logger.info(f"📋 Using individual settings:")
            logger.info(f"   REDIS_HOST: {REDIS_HOST}")
            logger.info(f"   REDIS_PORT: {REDIS_PORT}")
            logger.info(f"   REDIS_DB: {REDIS_DB}")
            logger.info(f"   REDIS_PASSWORD: {'***set***' if REDIS_PASSWORD else 'NOT set'}")
        
        try:
            # Prefer REDIS_URL (standard for cloud providers like Render)
            if REDIS_URL:
                from redis import ConnectionPool
                logger.info("🔌 Attempting connection via REDIS_URL...")
                pool = ConnectionPool.from_url(
                    REDIS_URL,
                    decode_responses=True,
                    socket_connect_timeout=10,
                    socket_timeout=10,
                    retry_on_timeout=True
                )
                self.redis_client = redis.Redis(connection_pool=pool)
            else:
                # Fallback to individual settings
                logger.info(f"🔌 Attempting connection via individual settings ({REDIS_HOST}:{REDIS_PORT})...")
                self.redis_client = redis.Redis(
                    host=REDIS_HOST,
                    port=REDIS_PORT,
                    db=REDIS_DB,
                    password=REDIS_PASSWORD,
                    decode_responses=True,
                    socket_connect_timeout=10,
                    socket_timeout=10,
                    retry_on_timeout=True
                )
            
            # Test connection with detailed logging
            logger.info("🧪 Testing Redis connection (ping)...")
            result = self.redis_client.ping()
            if result:
                self.use_redis = True
                logger.info("=" * 60)
                logger.info("✅ REDIS CONNECTION SUCCESSFUL")
                logger.info("=" * 60)
                # Get Redis info
                try:
                    info = self.redis_client.info('server')
                    logger.info(f"   Redis Version: {info.get('redis_version', 'unknown')}")
                    logger.info(f"   Redis Mode: {'Cluster' if 'cluster' in str(REDIS_URL or '').lower() else 'Standalone'}")
                except:
                    pass
            else:
                raise Exception("Ping returned False")
                
        except redis.ConnectionError as e:
            logger.error("=" * 60)
            logger.error("❌ REDIS CONNECTION FAILED - Connection Error")
            logger.error("=" * 60)
            logger.error(f"   Error: {str(e)}")
            logger.error("   🔧 Possible causes:")
            if REDIS_URL:
                logger.error("      - REDIS_URL is incorrect or malformed")
                logger.error("      - Redis service hasn't been created yet")
            else:
                logger.error(f"      - Cannot reach Redis at {REDIS_HOST}:{REDIS_PORT}")
                logger.error("      - Redis service is not running")
                logger.error("      - Network/firewall blocking connection")
            logger.error("   💡 Solution: Check Render Dashboard and ensure Redis service is created")
            logger.error("   ⚠️  Falling back to in-memory session storage (sessions will not persist)")
            self.use_redis = False
            self.redis_client = None
        except redis.TimeoutError as e:
            logger.error("=" * 60)
            logger.error("❌ REDIS CONNECTION FAILED - Timeout")
            logger.error("=" * 60)
            logger.error(f"   Error: {str(e)}")
            logger.error("   🔧 Possible causes: Redis is unreachable or slow")
            logger.error("   ⚠️  Falling back to in-memory session storage")
            self.use_redis = False
            self.redis_client = None
        except Exception as e:
            logger.error("=" * 60)
            logger.error("❌ REDIS CONNECTION FAILED - Unexpected Error")
            logger.error("=" * 60)
            logger.error(f"   Error Type: {type(e).__name__}")
            logger.error(f"   Error Message: {str(e)}")
            logger.error("   ⚠️  Falling back to in-memory session storage")
            self.use_redis = False
            self.redis_client = None
        
        logger.info("=" * 60)
    
    def _ensure_connection(self):
        """Reconnect if connection was lost"""
        if self.use_redis and not self.redis_client:
            self._connect_redis()
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve session data by session ID.
        Updates last_accessed_at timestamp.
        
        Args:
            session_id: Unique session identifier
            
        Returns:
            Session data dict or None if not found
        """
        self._ensure_connection()
        
        # Log session lookup attempt
        logger.info(f"🔍 Looking up session: {session_id[:8]}... (Redis: {self.use_redis})")
        
        if self.use_redis:
            try:
                key = f"{SESSION_PREFIX}{session_id}"
                data = self.redis_client.get(key)
                
                if data:
                    session_data = json.loads(data)
                    logger.info(f"✅ Session found in Redis: {session_id[:8]}...")
                    # Update last access time
                    session_data['last_accessed_at'] = datetime.now().isoformat()
                    # Save updated session
                    self.save_session(session_id, session_data)
                    return session_data
                else:
                    logger.warning(f"❌ Session NOT found in Redis: {session_id[:8]}...")
                    logger.warning(f"   Key searched: {key}")
                    # Check if any sessions exist
                    try:
                        all_keys = self.redis_client.keys(f"{SESSION_PREFIX}*")
                        logger.warning(f"   Total sessions in Redis: {len(all_keys)}")
                        if all_keys:
                            logger.warning(f"   Sample keys: {[k[:20] for k in all_keys[:3]]}")
                    except:
                        pass
                return None
            except Exception as e:
                logger.error(f"❌ Redis get error: {e}")
                logger.error(f"   Error type: {type(e).__name__}")
                # Fallback to in-memory
                fallback_data = self.fallback_store.get(session_id)
                if fallback_data:
                    logger.info(f"✅ Found session in fallback store: {session_id[:8]}...")
                return fallback_data
        else:
            # In-memory fallback
            session_data = self.fallback_store.get(session_id)
            if session_data:
                logger.info(f"✅ Session found in fallback: {session_id[:8]}...")
                session_data['last_accessed_at'] = datetime.now().isoformat()
            else:
                logger.warning(f"❌ Session NOT found in fallback: {session_id[:8]}...")
                logger.warning(f"   Fallback store has {len(self.fallback_store)} sessions")
            return session_data
    
    def save_session(self, session_id: str, data: Dict[str, Any], user_id: Optional[str] = None) -> bool:
        """
        Save session data to Redis.
        
        Args:
            session_id: Unique session identifier
            data: Session data dictionary
            user_id: Optional Firebase user ID to link session to user
            
        Returns:
            True if saved successfully, False otherwise
        """
        self._ensure_connection()
        
        # Ensure timestamps exist
        now = datetime.now().isoformat()
        data['last_accessed_at'] = now
        if 'created_at' not in data:
            data['created_at'] = now
        
        # Add user_id to session data if provided
        if user_id:
            data['user_id'] = user_id
        
        # Add history entry
        self.add_history(session_id, 'session_updated', data)
        
        if self.use_redis:
            try:
                key = f"{SESSION_PREFIX}{session_id}"
                ttl_seconds = SESSION_TIMEOUT_HOURS * 3600
                
                # Save session data
                serialized_data = json.dumps(data, default=str)
                self.redis_client.setex(
                    key,
                    ttl_seconds,
                    serialized_data
                )
                
                # Verify it was saved
                verify = self.redis_client.get(key)
                if verify:
                    logger.info(f"✅ Saved session {session_id[:8]}... to Redis (TTL: {ttl_seconds}s)")
                else:
                    logger.error(f"❌ Failed to verify session save: {session_id[:8]}...")
                
                # Update statistics
                self._update_stats(session_id, data)
                
                return True
            except Exception as e:
                logger.error(f"Redis save error: {e}")
                # Fallback to in-memory
                self.fallback_store[session_id] = data
                return False
        else:
            # In-memory fallback
            self.fallback_store[session_id] = data
            return True
    
    def delete_session(self, session_id: str) -> bool:
        """
        Delete a session from Redis.
        
        Args:
            session_id: Unique session identifier
            
        Returns:
            True if deleted successfully
        """
        self._ensure_connection()
        
        # Add history entry
        self.add_history(session_id, 'session_deleted', {})
        
        if self.use_redis:
            try:
                key = f"{SESSION_PREFIX}{session_id}"
                history_key = f"{HISTORY_PREFIX}{session_id}"
                stats_key = f"{STATS_PREFIX}{session_id}"
                
                self.redis_client.delete(key)
                self.redis_client.delete(history_key)
                self.redis_client.delete(stats_key)
                
                logger.info(f"Deleted session {session_id[:8]}... from Redis")
                return True
            except Exception as e:
                logger.error(f"Redis delete error: {e}")
                return False
        else:
            # In-memory fallback
            if session_id in self.fallback_store:
                del self.fallback_store[session_id]
            return True
    
    def add_history(self, session_id: str, event_type: str, data: Dict[str, Any]):
        """
        Add an entry to session history.
        
        Args:
            session_id: Session identifier
            event_type: Type of event (e.g., 'session_created', 'session_updated')
            data: Event data
        """
        self._ensure_connection()
        
        history_entry = {
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'data': data
        }
        
        if self.use_redis:
            try:
                history_key = f"{HISTORY_PREFIX}{session_id}"
                # Use Redis list to store history (keep last 100 entries)
                self.redis_client.lpush(history_key, json.dumps(history_entry, default=str))
                self.redis_client.ltrim(history_key, 0, 99)  # Keep only last 100 entries
                # Set expiration on history key
                self.redis_client.expire(history_key, SESSION_TIMEOUT_HOURS * 3600)
            except Exception as e:
                logger.error(f"Redis history error: {e}")
        else:
            # In-memory fallback for history
            if 'history' not in self.fallback_store:
                self.fallback_store['history'] = {}
            if session_id not in self.fallback_store['history']:
                self.fallback_store['history'][session_id] = []
            
            history_list = self.fallback_store['history'][session_id]
            history_list.insert(0, history_entry)
            # Keep only last 100 entries
            if len(history_list) > 100:
                history_list[:] = history_list[:100]
    
    def get_session_history(self, session_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get history for a specific session.
        
        Args:
            session_id: Session identifier
            limit: Maximum number of history entries to return
            
        Returns:
            List of history entries
        """
        self._ensure_connection()
        
        if self.use_redis:
            try:
                history_key = f"{HISTORY_PREFIX}{session_id}"
                entries = self.redis_client.lrange(history_key, 0, limit - 1)
                return [json.loads(entry) for entry in entries]
            except Exception as e:
                logger.error(f"Redis history get error: {e}")
                return []
        else:
            # In-memory fallback
            history = self.fallback_store.get('history', {}).get(session_id, [])
            return history[:limit]
    
    def get_all_sessions(self, limit: int = 100, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get all active sessions with metadata, optionally filtered by user.
        
        Args:
            limit: Maximum number of sessions to return
            user_id: Optional Firebase user ID to filter sessions by user
            
        Returns:
            List of session metadata
        """
        self._ensure_connection()
        
        sessions = []
        
        if self.use_redis:
            try:
                pattern = f"{SESSION_PREFIX}*"
                keys = self.redis_client.keys(pattern)[:limit]
                
                for key in keys:
                    session_id = key.replace(SESSION_PREFIX, "")
                    data = self.redis_client.get(key)
                    if data:
                        session_data = json.loads(data)
                        session_user_id = session_data.get('user_id')
                        
                        # Filter by user_id if provided
                        if user_id and session_user_id != user_id:
                            continue
                        
                        sessions.append({
                            'session_id': session_id,
                            'filename': session_data.get('filename', 'Unknown'),
                            'created_at': session_data.get('created_at'),
                            'last_accessed_at': session_data.get('last_accessed_at'),
                            'progress': len(session_data.get('filled_values', {})) / max(len(session_data.get('placeholders', [])), 1) * 100,
                            'status': session_data.get('status', 'active'),
                            'placeholders_count': len(session_data.get('placeholders', [])),
                            'filled_count': len(session_data.get('filled_values', {})),
                            'user_id': session_user_id
                        })
            except Exception as e:
                logger.error(f"Redis get_all_sessions error: {e}")
        else:
            # In-memory fallback
            for session_id, data in list(self.fallback_store.items())[:limit]:
                if session_id != 'history' and isinstance(data, dict):
                    session_user_id = data.get('user_id')
                    
                    # Filter by user_id if provided
                    if user_id and session_user_id != user_id:
                        continue
                    
                    sessions.append({
                        'session_id': session_id,
                        'filename': data.get('filename', 'Unknown'),
                        'created_at': data.get('created_at'),
                        'last_accessed_at': data.get('last_accessed_at'),
                        'progress': len(data.get('filled_values', {})) / max(len(data.get('placeholders', [])), 1) * 100,
                        'status': data.get('status', 'active'),
                        'placeholders_count': len(data.get('placeholders', [])),
                        'filled_count': len(data.get('filled_values', {})),
                        'user_id': session_user_id
                    })
        
        # Sort by last_accessed_at descending
        sessions.sort(key=lambda x: x.get('last_accessed_at', ''), reverse=True)
        return sessions
    
    def _update_stats(self, session_id: str, data: Dict[str, Any]):
        """Update session statistics"""
        self._ensure_connection()
        
        if self.use_redis:
            try:
                stats_key = f"{STATS_PREFIX}{session_id}"
                stats = {
                    'placeholders_count': len(data.get('placeholders', [])),
                    'filled_count': len(data.get('filled_values', {})),
                    'progress_percentage': len(data.get('filled_values', {})) / max(len(data.get('placeholders', [])), 1) * 100,
                    'last_updated': datetime.now().isoformat()
                }
                self.redis_client.setex(
                    stats_key,
                    SESSION_TIMEOUT_HOURS * 3600,
                    json.dumps(stats)
                )
            except Exception as e:
                logger.error(f"Redis stats update error: {e}")
    
    def get_session_stats(self) -> Dict[str, Any]:
        """
        Get overall session statistics.
        
        Returns:
            Dictionary with statistics
        """
        self._ensure_connection()
        
        sessions = self.get_all_sessions(limit=1000)
        
        stats = {
            'total_sessions': len(sessions),
            'active_sessions': len([s for s in sessions if s.get('status') == 'active']),
            'completed_sessions': len([s for s in sessions if s.get('status') == 'completed']),
            'average_progress': sum(s.get('progress', 0) for s in sessions) / max(len(sessions), 1),
            'total_placeholders': sum(s.get('placeholders_count', 0) for s in sessions),
            'total_filled': sum(s.get('filled_count', 0) for s in sessions)
        }
        
        return stats
    
    def cleanup_expired_sessions(self) -> int:
        """
        Clean up expired sessions (Redis handles this automatically via TTL,
        but this method can be used for manual cleanup).
        
        Returns:
            Number of sessions cleaned up
        """
        # Redis handles expiration automatically via TTL
        # This method is mainly for in-memory fallback
        if not self.use_redis:
            current_time = datetime.now()
            expired = []
            
            for session_id, data in list(self.fallback_store.items()):
                if session_id == 'history':
                    continue
                    
                last_access = data.get('last_accessed_at')
                if last_access:
                    try:
                        last_access_dt = datetime.fromisoformat(last_access)
                        if (current_time - last_access_dt) > timedelta(hours=SESSION_TIMEOUT_HOURS):
                            expired.append(session_id)
                    except:
                        pass
            
            for session_id in expired:
                del self.fallback_store[session_id]
                if 'history' in self.fallback_store and session_id in self.fallback_store['history']:
                    del self.fallback_store['history'][session_id]
            
            return len(expired)
        
        return 0


# Create global session manager instance
session_manager = SessionManager()

