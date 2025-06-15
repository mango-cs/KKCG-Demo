import redis.asyncio as redis
import json
import pickle
from typing import Any, Optional, Union
import logging
from datetime import timedelta

from app.core.config import settings

logger = logging.getLogger(__name__)

class RedisClient:
    """Async Redis client with caching utilities"""
    
    def __init__(self):
        self.redis: Optional[redis.Redis] = None
        self.connected = False
    
    async def connect(self):
        """Initialize Redis connection"""
        try:
            self.redis = redis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5,
                retry_on_timeout=True,
                health_check_interval=30
            )
            
            # Test connection
            await self.redis.ping()
            self.connected = True
            logger.info("✅ Redis connection established")
            
        except Exception as e:
            logger.error(f"❌ Redis connection failed: {e}")
            self.connected = False
            raise
    
    async def disconnect(self):
        """Close Redis connection"""
        if self.redis:
            await self.redis.close()
            self.connected = False
            logger.info("Redis connection closed")
    
    async def ping(self):
        """Ping Redis server"""
        if not self.redis:
            await self.connect()
        return await self.redis.ping()
    
    async def get(self, key: str) -> Optional[str]:
        """Get value by key"""
        if not self.redis:
            await self.connect()
        try:
            return await self.redis.get(key)
        except Exception as e:
            logger.error(f"Redis GET error for key {key}: {e}")
            return None
    
    async def set(
        self, 
        key: str, 
        value: Union[str, int, float, dict, list], 
        ttl: Optional[int] = None
    ) -> bool:
        """Set value with optional TTL"""
        if not self.redis:
            await self.connect()
        
        try:
            # Convert complex types to JSON
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            elif not isinstance(value, str):
                value = str(value)
            
            if ttl:
                return await self.redis.setex(key, ttl, value)
            else:
                return await self.redis.set(key, value)
        except Exception as e:
            logger.error(f"Redis SET error for key {key}: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete key"""
        if not self.redis:
            await self.connect()
        try:
            return bool(await self.redis.delete(key))
        except Exception as e:
            logger.error(f"Redis DELETE error for key {key}: {e}")
            return False
    
    async def exists(self, key: str) -> bool:
        """Check if key exists"""
        if not self.redis:
            await self.connect()
        try:
            return bool(await self.redis.exists(key))
        except Exception as e:
            logger.error(f"Redis EXISTS error for key {key}: {e}")
            return False
    
    async def get_json(self, key: str) -> Optional[Union[dict, list]]:
        """Get JSON value by key"""
        value = await self.get(key)
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error for key {key}: {e}")
        return None
    
    async def set_json(
        self, 
        key: str, 
        value: Union[dict, list], 
        ttl: Optional[int] = None
    ) -> bool:
        """Set JSON value with optional TTL"""
        try:
            json_value = json.dumps(value)
            return await self.set(key, json_value, ttl)
        except Exception as e:
            logger.error(f"JSON encode error for key {key}: {e}")
            return False
    
    async def increment(self, key: str, amount: int = 1) -> int:
        """Increment counter"""
        if not self.redis:
            await self.connect()
        try:
            return await self.redis.incrby(key, amount)
        except Exception as e:
            logger.error(f"Redis INCREMENT error for key {key}: {e}")
            return 0
    
    async def expire(self, key: str, seconds: int) -> bool:
        """Set expiration for key"""
        if not self.redis:
            await self.connect()
        try:
            return await self.redis.expire(key, seconds)
        except Exception as e:
            logger.error(f"Redis EXPIRE error for key {key}: {e}")
            return False
    
    async def ttl(self, key: str) -> int:
        """Get TTL for key"""
        if not self.redis:
            await self.connect()
        try:
            return await self.redis.ttl(key)
        except Exception as e:
            logger.error(f"Redis TTL error for key {key}: {e}")
            return -1
    
    async def flush_pattern(self, pattern: str) -> int:
        """Delete all keys matching pattern"""
        if not self.redis:
            await self.connect()
        try:
            keys = await self.redis.keys(pattern)
            if keys:
                return await self.redis.delete(*keys)
            return 0
        except Exception as e:
            logger.error(f"Redis FLUSH_PATTERN error for pattern {pattern}: {e}")
            return 0
    
    # Caching utilities
    async def cache_forecast(
        self, 
        dish_id: str, 
        outlet_id: str, 
        forecast_data: dict,
        ttl: int = None
    ) -> bool:
        """Cache forecast data"""
        key = f"forecast:{dish_id}:{outlet_id}"
        ttl = ttl or settings.FORECAST_CACHE_TTL
        return await self.set_json(key, forecast_data, ttl)
    
    async def get_cached_forecast(
        self, 
        dish_id: str, 
        outlet_id: str
    ) -> Optional[dict]:
        """Get cached forecast data"""
        key = f"forecast:{dish_id}:{outlet_id}"
        return await self.get_json(key)
    
    async def cache_model_metrics(
        self, 
        model_name: str, 
        metrics: dict,
        ttl: int = None
    ) -> bool:
        """Cache model performance metrics"""
        key = f"model_metrics:{model_name}"
        ttl = ttl or settings.CACHE_TTL
        return await self.set_json(key, metrics, ttl)
    
    async def get_cached_model_metrics(self, model_name: str) -> Optional[dict]:
        """Get cached model metrics"""
        key = f"model_metrics:{model_name}"
        return await self.get_json(key)
    
    async def cache_user_session(
        self, 
        user_id: str, 
        session_data: dict,
        ttl: int = None
    ) -> bool:
        """Cache user session data"""
        key = f"session:{user_id}"
        ttl = ttl or 3600  # 1 hour default
        return await self.set_json(key, session_data, ttl)
    
    async def get_user_session(self, user_id: str) -> Optional[dict]:
        """Get user session data"""
        key = f"session:{user_id}"
        return await self.get_json(key)
    
    async def invalidate_user_session(self, user_id: str) -> bool:
        """Invalidate user session"""
        key = f"session:{user_id}"
        return await self.delete(key)
    
    async def rate_limit_check(
        self, 
        identifier: str, 
        limit: int, 
        window: int
    ) -> tuple[bool, int]:
        """Check rate limit for identifier"""
        key = f"rate_limit:{identifier}"
        
        try:
            current = await self.get(key)
            if current is None:
                await self.set(key, "1", window)
                return True, 1
            
            current_count = int(current)
            if current_count >= limit:
                ttl = await self.ttl(key)
                return False, ttl
            
            await self.increment(key)
            return True, current_count + 1
            
        except Exception as e:
            logger.error(f"Rate limit check error for {identifier}: {e}")
            return True, 0  # Allow on error
    
    async def health_check(self) -> bool:
        """Health check for Redis"""
        try:
            await self.ping()
            return True
        except Exception:
            return False

# Create global Redis client instance
redis_client = RedisClient() 