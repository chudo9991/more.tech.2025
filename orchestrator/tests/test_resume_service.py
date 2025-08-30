"""
Unit tests for ResumeService
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from sqlalchemy.orm import Session
from datetime import datetime

from app.services.resume_service import ResumeService
from app.models import Resume, Vacancy
from app.schemas.resume import ResumeCreate


class TestResumeService:
    """Test cases for ResumeService"""
    
    @pytest.fixture
    def mock_db(self):
        """Mock database session"""
        return Mock(spec=Session)
    
    @pytest.fixture
    def resume_service(self, mock_db):
        """ResumeService instance with mocked dependencies"""
        return ResumeService(mock_db)
    
    @pytest.fixture
    def sample_resume_data(self):
        """Sample resume data for testing"""
        return {
            "filename": "test_resume.pdf",
            "original_filename": "resume.pdf",
            "file_type": "pdf",
            "file_size": 1024,
            "vacancy_id": "test_vacancy_001",
            "status": "uploaded"
        }
    
    @pytest.fixture
    def sample_resume(self, sample_resume_data):
        """Sample Resume model instance"""
        resume = Resume(
            id="test_resume_001",
            **sample_resume_data,
            upload_date=datetime.now(),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        return resume
    
    def test_create_resume_success(self, resume_service, mock_db, sample_resume_data):
        """Test successful resume creation"""
        # Arrange
        resume_create = ResumeCreate(**sample_resume_data)
        mock_db.add.return_value = None
        mock_db.commit.return_value = None
        mock_db.refresh.return_value = None
        
        # Act
        result = resume_service.create_resume(resume_create)
        
        # Assert
        assert result is not None
        assert result.filename == sample_resume_data["filename"]
        assert result.original_filename == sample_resume_data["original_filename"]
        assert result.file_type == sample_resume_data["file_type"]
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()
    
    def test_get_resume_success(self, resume_service, mock_db, sample_resume):
        """Test successful resume retrieval"""
        # Arrange
        resume_id = "test_resume_001"
        mock_db.query.return_value.filter.return_value.first.return_value = sample_resume
        
        # Act
        result = resume_service.get_resume(resume_id)
        
        # Assert
        assert result is not None
        assert result.id == resume_id
        assert result.filename == sample_resume.filename
    
    def test_get_resume_not_found(self, resume_service, mock_db):
        """Test resume retrieval when not found"""
        # Arrange
        resume_id = "nonexistent_resume"
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        # Act
        result = resume_service.get_resume(resume_id)
        
        # Assert
        assert result is None
    
    def test_get_resumes_with_pagination(self, resume_service, mock_db, sample_resume):
        """Test resume list retrieval with pagination"""
        # Arrange
        mock_query = Mock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.offset.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.all.return_value = [sample_resume]
        mock_query.count.return_value = 1
        
        # Act
        result = resume_service.get_resumes(skip=0, limit=10)
        
        # Assert
        assert result is not None
        assert "resumes" in result
        assert "total" in result
        assert "page" in result
        assert "size" in result
        assert "total_pages" in result
        assert len(result["resumes"]) == 1
    
    def test_get_resume_statistics(self, resume_service, mock_db):
        """Test resume statistics calculation"""
        # Arrange
        mock_query = Mock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.count.return_value = 5
        mock_query.scalar.return_value = 75.5
        
        # Mock cache service
        with patch('app.services.resume_service.cache_service') as mock_cache:
            mock_cache.get_statistics.return_value = None
            mock_cache.set_statistics.return_value = True
            
            # Act
            result = resume_service.get_resume_statistics()
            
            # Assert
            assert result is not None
            assert "total_resumes" in result
            assert "processed_resumes" in result
            assert "error_resumes" in result
            assert "average_score" in result
            assert "score_distribution" in result
            assert "top_vacancies" in result
    
    @pytest.mark.asyncio
    async def test_process_resume_success(self, resume_service, mock_db, sample_resume):
        """Test successful resume processing"""
        # Arrange
        resume_id = "test_resume_001"
        mock_db.query.return_value.filter.return_value.first.return_value = sample_resume
        mock_db.commit.return_value = None
        
        # Mock file storage
        with patch('app.services.resume_service.file_storage') as mock_storage:
            mock_storage.download_file.return_value = Mock()
            
            # Mock text extraction
            with patch('app.services.resume_service.text_extractor') as mock_extractor:
                mock_extractor.extract_text.return_value = {
                    "success": True,
                    "text": "Sample resume text"
                }
                
                # Mock resume parser
                with patch('app.services.resume_service.resume_parser') as mock_parser:
                    mock_parser.parse_resume.return_value = {
                        "success": True,
                        "sections": [],
                        "skills": [],
                        "summary": {
                            "total_sections": 5,
                            "total_skills": 10,
                            "experience_years": 3,
                            "education_level": "bachelor"
                        }
                    }
                    
                    # Act
                    result = await resume_service.process_resume(resume_id)
                    
                    # Assert
                    assert result is not None
                    assert result["success"] is True
                    assert "resume_id" in result
                    assert "sections_found" in result
                    assert "skills_found" in result
    
    @pytest.mark.asyncio
    async def test_process_resume_not_found(self, resume_service, mock_db):
        """Test resume processing when resume not found"""
        # Arrange
        resume_id = "nonexistent_resume"
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        # Act & Assert
        with pytest.raises(Exception, match="Resume not found"):
            await resume_service.process_resume(resume_id)
    
    @pytest.mark.asyncio
    async def test_calculate_resume_score_success(self, resume_service, mock_db, sample_resume):
        """Test successful resume score calculation"""
        # Arrange
        resume_id = "test_resume_001"
        sample_resume.vacancy_id = "test_vacancy_001"
        mock_db.query.return_value.filter.return_value.first.return_value = sample_resume
        mock_db.commit.return_value = None
        
        # Mock cache service
        with patch('app.services.resume_service.cache_service') as mock_cache:
            mock_cache.get_resume_score.return_value = None
            mock_cache.set_resume_score.return_value = True
            
            # Mock relevance scorer
            with patch('app.services.resume_service.relevance_scorer') as mock_scorer:
                mock_scorer.calculate_resume_score.return_value = {
                    "total_score": 85.5,
                    "confidence_score": 0.9,
                    "component_scores": {}
                }
                
                # Act
                result = await resume_service.calculate_resume_score(resume_id)
                
                # Assert
                assert result is not None
                assert result["success"] is True
                assert "resume_id" in result
                assert "total_score" in result
                assert "confidence_score" in result
    
    def test_delete_resume_success(self, resume_service, mock_db, sample_resume):
        """Test successful resume deletion"""
        # Arrange
        resume_id = "test_resume_001"
        mock_db.query.return_value.filter.return_value.first.return_value = sample_resume
        mock_db.delete.return_value = None
        mock_db.commit.return_value = None
        
        # Mock file storage
        with patch('app.services.resume_service.file_storage') as mock_storage:
            mock_storage.delete_file.return_value = True
            
            # Act
            result = resume_service.delete_resume(resume_id)
            
            # Assert
            assert result is True
            mock_db.delete.assert_called_once_with(sample_resume)
            mock_db.commit.assert_called_once()
    
    def test_delete_resume_not_found(self, resume_service, mock_db):
        """Test resume deletion when not found"""
        # Arrange
        resume_id = "nonexistent_resume"
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        # Act & Assert
        with pytest.raises(Exception, match="Resume not found"):
            resume_service.delete_resume(resume_id)
