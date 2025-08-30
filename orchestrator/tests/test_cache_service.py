"""
Unit tests for CacheService
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import json
from datetime import datetime

from app.services.cache_service import CacheService


class TestCacheService:
    """Test cases for CacheService"""
    
    @pytest.fixture
    def mock_redis(self):
        """Mock Redis client"""
        return Mock()
    
    @pytest.fixture
    def cache_service(self, mock_redis):
        """CacheService instance with mocked Redis"""
        with patch('app.services.cache_service.redis.Redis') as mock_redis_class:
            mock_redis_class.return_value = mock_redis
            return CacheService()
    
    def test_generate_key(self, cache_service):
        """Test cache key generation"""
        # Act
        key = cache_service._generate_key("resume_analysis", "resume_001")
        
        # Assert
        assert key == "resume:analysis:resume_001"
    
    def test_generate_hash(self, cache_service):
        """Test hash generation for data"""
        # Arrange
        test_data = {"key": "value", "number": 123}
        
        # Act
        hash_value = cache_service._generate_hash(test_data)
        
        # Assert
        assert isinstance(hash_value, str)
        assert len(hash_value) == 32  # MD5 hash length
    
    def test_set_and_get_success(self, cache_service, mock_redis):
        """Test successful set and get operations"""
        # Arrange
        test_data = {"test": "data", "number": 42}
        mock_redis.setex.return_value = True
        mock_redis.get.return_value = json.dumps({
            "data": test_data,
            "cached_at": "2024-01-01T00:00:00",
            "ttl": 3600
        })
        
        # Act - Set
        set_result = cache_service.set("resume_analysis", "resume_001", test_data)
        
        # Assert - Set
        assert set_result is True
        mock_redis.setex.assert_called_once()
        
        # Act - Get
        get_result = cache_service.get("resume_analysis", "resume_001")
        
        # Assert - Get
        assert get_result is not None
        assert get_result["data"] == test_data
        assert "cached_at" in get_result
        assert "ttl" in get_result
    
    def test_get_not_found(self, cache_service, mock_redis):
        """Test get operation when key not found"""
        # Arrange
        mock_redis.get.return_value = None
        
        # Act
        result = cache_service.get("resume_analysis", "nonexistent")
        
        # Assert
        assert result is None
    
    def test_get_with_exception(self, cache_service, mock_redis):
        """Test get operation with Redis exception"""
        # Arrange
        mock_redis.get.side_effect = Exception("Redis connection error")
        
        # Act
        result = cache_service.get("resume_analysis", "resume_001")
        
        # Assert
        assert result is None
    
    def test_set_with_exception(self, cache_service, mock_redis):
        """Test set operation with Redis exception"""
        # Arrange
        test_data = {"test": "data"}
        mock_redis.setex.side_effect = Exception("Redis connection error")
        
        # Act
        result = cache_service.set("resume_analysis", "resume_001", test_data)
        
        # Assert
        assert result is False
    
    def test_delete_success(self, cache_service, mock_redis):
        """Test successful delete operation"""
        # Arrange
        mock_redis.delete.return_value = 1
        
        # Act
        result = cache_service.delete("resume_analysis", "resume_001")
        
        # Assert
        assert result is True
        mock_redis.delete.assert_called_once()
    
    def test_delete_not_found(self, cache_service, mock_redis):
        """Test delete operation when key not found"""
        # Arrange
        mock_redis.delete.return_value = 0
        
        # Act
        result = cache_service.delete("resume_analysis", "nonexistent")
        
        # Assert
        assert result is False
    
    def test_clear_prefix_success(self, cache_service, mock_redis):
        """Test successful clear prefix operation"""
        # Arrange
        mock_redis.keys.return_value = ["resume:analysis:key1", "resume:analysis:key2"]
        mock_redis.delete.return_value = 2
        
        # Act
        result = cache_service.clear_prefix("resume_analysis")
        
        # Assert
        assert result is True
        mock_redis.keys.assert_called_once_with("resume:analysis:*")
        mock_redis.delete.assert_called_once_with("resume:analysis:key1", "resume:analysis:key2")
    
    def test_clear_prefix_no_keys(self, cache_service, mock_redis):
        """Test clear prefix operation when no keys found"""
        # Arrange
        mock_redis.keys.return_value = []
        
        # Act
        result = cache_service.clear_prefix("resume_analysis")
        
        # Assert
        assert result is True
        mock_redis.keys.assert_called_once()
        mock_redis.delete.assert_not_called()
    
    def test_get_resume_analysis(self, cache_service, mock_redis):
        """Test get resume analysis from cache"""
        # Arrange
        test_data = {"analysis": "result"}
        mock_redis.get.return_value = json.dumps({
            "data": test_data,
            "cached_at": "2024-01-01T00:00:00",
            "ttl": 3600
        })
        
        # Act
        result = cache_service.get_resume_analysis("resume_001")
        
        # Assert
        assert result == test_data
    
    def test_set_resume_analysis(self, cache_service, mock_redis):
        """Test set resume analysis to cache"""
        # Arrange
        test_data = {"analysis": "result"}
        mock_redis.setex.return_value = True
        
        # Act
        result = cache_service.set_resume_analysis("resume_001", test_data)
        
        # Assert
        assert result is True
        mock_redis.setex.assert_called_once()
    
    def test_get_vacancy_requirements(self, cache_service, mock_redis):
        """Test get vacancy requirements from cache"""
        # Arrange
        test_data = {"requirements": ["Python", "SQL"]}
        mock_redis.get.return_value = json.dumps({
            "data": test_data,
            "cached_at": "2024-01-01T00:00:00",
            "ttl": 3600
        })
        
        # Act
        result = cache_service.get_vacancy_requirements("vacancy_001")
        
        # Assert
        assert result == test_data
    
    def test_set_vacancy_requirements(self, cache_service, mock_redis):
        """Test set vacancy requirements to cache"""
        # Arrange
        test_data = {"requirements": ["Python", "SQL"]}
        mock_redis.setex.return_value = True
        
        # Act
        result = cache_service.set_vacancy_requirements("vacancy_001", test_data)
        
        # Assert
        assert result is True
        mock_redis.setex.assert_called_once()
    
    def test_get_resume_score(self, cache_service, mock_redis):
        """Test get resume score from cache"""
        # Arrange
        test_data = {"total_score": 85.5, "confidence_score": 0.9}
        mock_redis.get.return_value = json.dumps({
            "data": test_data,
            "cached_at": "2024-01-01T00:00:00",
            "ttl": 3600
        })
        
        # Act
        result = cache_service.get_resume_score("resume_001")
        
        # Assert
        assert result == test_data
    
    def test_set_resume_score(self, cache_service, mock_redis):
        """Test set resume score to cache"""
        # Arrange
        test_data = {"total_score": 85.5, "confidence_score": 0.9}
        mock_redis.setex.return_value = True
        
        # Act
        result = cache_service.set_resume_score("resume_001", test_data)
        
        # Assert
        assert result is True
        mock_redis.setex.assert_called_once()
    
    def test_get_statistics(self, cache_service, mock_redis):
        """Test get statistics from cache"""
        # Arrange
        test_data = {"total": 100, "processed": 80}
        mock_redis.get.return_value = json.dumps({
            "data": test_data,
            "cached_at": "2024-01-01T00:00:00",
            "ttl": 3600
        })
        
        # Act
        result = cache_service.get_statistics("resume_overview")
        
        # Assert
        assert result == test_data
    
    def test_set_statistics(self, cache_service, mock_redis):
        """Test set statistics to cache"""
        # Arrange
        test_data = {"total": 100, "processed": 80}
        mock_redis.setex.return_value = True
        
        # Act
        result = cache_service.set_statistics("resume_overview", test_data)
        
        # Assert
        assert result is True
        mock_redis.setex.assert_called_once()
    
    def test_invalidate_resume_cache(self, cache_service, mock_redis):
        """Test invalidate resume cache"""
        # Arrange
        mock_redis.delete.return_value = 1
        mock_redis.keys.return_value = ["stats:key1", "stats:key2"]
        
        # Act
        result = cache_service.invalidate_resume_cache("resume_001")
        
        # Assert
        assert result is True
        # Should call delete for resume analysis and score
        assert mock_redis.delete.call_count >= 2
        # Should call keys and delete for statistics
        mock_redis.keys.assert_called_once_with("stats:*")
    
    def test_invalidate_vacancy_cache(self, cache_service, mock_redis):
        """Test invalidate vacancy cache"""
        # Arrange
        mock_redis.delete.return_value = 1
        mock_redis.keys.return_value = ["resume:score:key1", "stats:key1"]
        
        # Act
        result = cache_service.invalidate_vacancy_cache("vacancy_001")
        
        # Assert
        assert result is True
        # Should call delete for vacancy requirements
        mock_redis.delete.assert_called()
        # Should call keys and delete for resume scores and statistics
        assert mock_redis.keys.call_count >= 2
    
    def test_get_cache_info(self, cache_service, mock_redis):
        """Test get cache information"""
        # Arrange
        mock_redis.keys.side_effect = [
            ["resume:analysis:key1", "resume:analysis:key2"],  # resume_analysis
            ["vacancy:req:key1"],  # vacancy_requirements
            ["resume:score:key1", "resume:score:key2"],  # resume_score
            ["stats:key1"],  # statistics
            ["file:proc:key1"],  # file_processing
            ["resume:analysis:key1", "resume:analysis:key2", "vacancy:req:key1"]  # total
        ]
        mock_redis.info.return_value = {"used_memory": "1MB", "total_memory": "10MB"}
        
        # Act
        result = cache_service.get_cache_info()
        
        # Assert
        assert result is not None
        assert "resume_analysis" in result
        assert "vacancy_requirements" in result
        assert "resume_score" in result
        assert "statistics" in result
        assert "file_processing" in result
        assert "total_keys" in result
        assert "memory_usage" in result
        assert result["resume_analysis"] == 2
        assert result["vacancy_requirements"] == 1
        assert result["resume_score"] == 2
        assert result["statistics"] == 1
        assert result["file_processing"] == 1
        assert result["total_keys"] == 3
    
    def test_health_check_success(self, cache_service, mock_redis):
        """Test successful health check"""
        # Arrange
        mock_redis.ping.return_value = True
        
        # Act
        result = cache_service.health_check()
        
        # Assert
        assert result is True
        mock_redis.ping.assert_called_once()
    
    def test_health_check_failure(self, cache_service, mock_redis):
        """Test health check failure"""
        # Arrange
        mock_redis.ping.side_effect = Exception("Connection failed")
        
        # Act
        result = cache_service.health_check()
        
        # Assert
        assert result is False
