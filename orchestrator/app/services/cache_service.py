"""
Cache service for performance optimization
"""
import json
import hashlib
from typing import Any, Optional, Dict
from datetime import datetime, timedelta
import redis
from app.core.config import settings


class CacheService:
    """Service for caching analysis results and frequently accessed data"""
    
    def __init__(self):
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            decode_responses=True
        )
        
        # Cache prefixes for different types of data
        self.prefixes = {
            'resume_analysis': 'resume:analysis:',
            'vacancy_requirements': 'vacancy:req:',
            'resume_score': 'resume:score:',
            'statistics': 'stats:',
            'file_processing': 'file:proc:'
        }
        
        # Default TTL for different cache types (in seconds)
        self.ttl = {
            'resume_analysis': 3600 * 24,  # 24 hours
            'vacancy_requirements': 3600 * 12,  # 12 hours
            'resume_score': 3600 * 6,  # 6 hours
            'statistics': 300,  # 5 minutes
            'file_processing': 3600  # 1 hour
        }
    
    def _generate_key(self, prefix: str, identifier: str) -> str:
        """Generate cache key with prefix"""
        return f"{self.prefixes[prefix]}{identifier}"
    
    def _generate_hash(self, data: Any) -> str:
        """Generate hash for data to use as cache key"""
        if isinstance(data, dict):
            data_str = json.dumps(data, sort_keys=True)
        else:
            data_str = str(data)
        return hashlib.md5(data_str.encode()).hexdigest()
    
    def get(self, prefix: str, identifier: str) -> Optional[Dict[str, Any]]:
        """
        Get cached data
        
        Args:
            prefix: Cache prefix (resume_analysis, vacancy_requirements, etc.)
            identifier: Unique identifier for the data
            
        Returns:
            Cached data or None if not found
        """
        try:
            key = self._generate_key(prefix, identifier)
            data = self.redis_client.get(key)
            
            if data:
                return json.loads(data)
            return None
            
        except Exception as e:
            print(f"Cache get error: {e}")
            return None
    
    def set(self, prefix: str, identifier: str, data: Any, ttl: Optional[int] = None) -> bool:
        """
        Set cached data
        
        Args:
            prefix: Cache prefix
            identifier: Unique identifier
            data: Data to cache
            ttl: Time to live in seconds (uses default if not specified)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            key = self._generate_key(prefix, identifier)
            cache_ttl = ttl or self.ttl.get(prefix, 3600)
            
            # Add timestamp to cached data
            cache_data = {
                'data': data,
                'cached_at': datetime.now().isoformat(),
                'ttl': cache_ttl
            }
            
            self.redis_client.setex(
                key,
                cache_ttl,
                json.dumps(cache_data, default=str)
            )
            return True
            
        except Exception as e:
            print(f"Cache set error: {e}")
            return False
    
    def delete(self, prefix: str, identifier: str) -> bool:
        """
        Delete cached data
        
        Args:
            prefix: Cache prefix
            identifier: Unique identifier
            
        Returns:
            True if successful, False otherwise
        """
        try:
            key = self._generate_key(prefix, identifier)
            return bool(self.redis_client.delete(key))
            
        except Exception as e:
            print(f"Cache delete error: {e}")
            return False
    
    def clear_prefix(self, prefix: str) -> bool:
        """
        Clear all cached data with specific prefix
        
        Args:
            prefix: Cache prefix to clear
            
        Returns:
            True if successful, False otherwise
        """
        try:
            pattern = f"{self.prefixes[prefix]}*"
            keys = self.redis_client.keys(pattern)
            
            if keys:
                self.redis_client.delete(*keys)
            return True
            
        except Exception as e:
            print(f"Cache clear prefix error: {e}")
            return False
    
    def get_resume_analysis(self, resume_id: str) -> Optional[Dict[str, Any]]:
        """Get cached resume analysis"""
        cached = self.get('resume_analysis', resume_id)
        if cached:
            return cached.get('data')
        return None
    
    def set_resume_analysis(self, resume_id: str, analysis_data: Dict[str, Any]) -> bool:
        """Set cached resume analysis"""
        return self.set('resume_analysis', resume_id, analysis_data)
    
    def get_vacancy_requirements(self, vacancy_id: str) -> Optional[Dict[str, Any]]:
        """Get cached vacancy requirements"""
        cached = self.get('vacancy_requirements', vacancy_id)
        if cached:
            return cached.get('data')
        return None
    
    def set_vacancy_requirements(self, vacancy_id: str, requirements: Dict[str, Any]) -> bool:
        """Set cached vacancy requirements"""
        return self.set('vacancy_requirements', vacancy_id, requirements)
    
    def get_resume_score(self, resume_id: str) -> Optional[Dict[str, Any]]:
        """Get cached resume score"""
        cached = self.get('resume_score', resume_id)
        if cached:
            return cached.get('data')
        return None
    
    def set_resume_score(self, resume_id: str, score_data: Dict[str, Any]) -> bool:
        """Set cached resume score"""
        return self.set('resume_score', resume_id, score_data)
    
    def get_statistics(self, stat_type: str) -> Optional[Dict[str, Any]]:
        """Get cached statistics"""
        cached = self.get('statistics', stat_type)
        if cached:
            return cached.get('data')
        return None
    
    def set_statistics(self, stat_type: str, stats_data: Dict[str, Any]) -> bool:
        """Set cached statistics"""
        return self.set('statistics', stat_type, stats_data)
    
    def invalidate_resume_cache(self, resume_id: str) -> bool:
        """Invalidate all cache related to specific resume"""
        try:
            # Delete resume analysis cache
            self.delete('resume_analysis', resume_id)
            # Delete resume score cache
            self.delete('resume_score', resume_id)
            # Clear statistics cache
            self.clear_prefix('statistics')
            return True
        except Exception as e:
            print(f"Cache invalidation error: {e}")
            return False
    
    def invalidate_vacancy_cache(self, vacancy_id: str) -> bool:
        """Invalidate all cache related to specific vacancy"""
        try:
            # Delete vacancy requirements cache
            self.delete('vacancy_requirements', vacancy_id)
            # Clear resume scores cache (they depend on vacancy requirements)
            self.clear_prefix('resume_score')
            # Clear statistics cache
            self.clear_prefix('statistics')
            return True
        except Exception as e:
            print(f"Cache invalidation error: {e}")
            return False
    
    def get_cache_info(self) -> Dict[str, Any]:
        """Get cache statistics and information"""
        try:
            info = {}
            for prefix_name, prefix in self.prefixes.items():
                keys = self.redis_client.keys(f"{prefix}*")
                info[prefix_name] = len(keys)
            
            info['total_keys'] = len(self.redis_client.keys('*'))
            info['memory_usage'] = self.redis_client.info('memory')
            
            return info
        except Exception as e:
            print(f"Cache info error: {e}")
            return {}
    
    def health_check(self) -> bool:
        """Check if cache service is healthy"""
        try:
            self.redis_client.ping()
            return True
        except Exception:
            return False


# Global instance
cache_service = CacheService()
