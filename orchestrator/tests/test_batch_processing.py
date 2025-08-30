"""
Unit tests for BatchProcessingService
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from sqlalchemy.orm import Session
from datetime import datetime

from app.services.batch_processing_service import BatchProcessingService


class TestBatchProcessingService:
    """Test cases for BatchProcessingService"""
    
    @pytest.fixture
    def mock_db(self):
        """Mock database session"""
        return Mock(spec=Session)
    
    @pytest.fixture
    def batch_service(self, mock_db):
        """BatchProcessingService instance with mocked dependencies"""
        return BatchProcessingService(mock_db)
    
    @pytest.fixture
    def sample_files_data(self):
        """Sample files data for testing"""
        return [
            {
                "filename": "resume1.pdf",
                "content": b"PDF content 1",
                "file_type": "pdf"
            },
            {
                "filename": "resume2.docx",
                "content": b"DOCX content 2",
                "file_type": "docx"
            }
        ]
    
    @pytest.fixture
    def sample_vacancy(self):
        """Sample vacancy for testing"""
        return Mock(id="test_vacancy_001", title="Test Vacancy")
    
    @pytest.mark.asyncio
    async def test_process_batch_upload_success(self, batch_service, mock_db, sample_files_data, sample_vacancy):
        """Test successful batch upload processing"""
        # Arrange
        vacancy_id = "test_vacancy_001"
        mock_db.query.return_value.filter.return_value.first.return_value = sample_vacancy
        
        # Mock cache service
        with patch('app.services.batch_processing_service.cache_service') as mock_cache:
            mock_cache.set.return_value = True
            mock_cache.clear_prefix.return_value = True
            mock_cache.invalidate_vacancy_cache.return_value = True
            
            # Mock resume service
            with patch.object(batch_service, 'resume_service') as mock_resume_service:
                mock_resume_service.create_resume.return_value = Mock(id="resume_001")
                mock_resume_service.process_resume.return_value = {
                    "success": True,
                    "sections_found": 5,
                    "skills_found": 10
                }
                
                # Mock file storage
                with patch('app.services.batch_processing_service.file_storage') as mock_storage:
                    mock_storage.upload_file.return_value = True
                    
                    # Act
                    result = await batch_service.process_batch_upload(
                        sample_files_data, 
                        vacancy_id, 
                        max_concurrent=2
                    )
                    
                    # Assert
                    assert result is not None
                    assert result["status"] == "completed"
                    assert result["total_files"] == 2
                    assert result["successful"] == 2
                    assert result["failed"] == 0
                    assert "batch_id" in result
                    assert "processing_time_seconds" in result
                    assert len(result["results"]) == 2
    
    @pytest.mark.asyncio
    async def test_process_batch_upload_with_errors(self, batch_service, mock_db, sample_files_data):
        """Test batch upload processing with some errors"""
        # Arrange
        # Mock cache service
        with patch('app.services.batch_processing_service.cache_service') as mock_cache:
            mock_cache.set.return_value = True
            mock_cache.clear_prefix.return_value = True
            
            # Mock resume service to throw error for first file
            with patch.object(batch_service, 'resume_service') as mock_resume_service:
                mock_resume_service.create_resume.side_effect = [
                    Exception("File processing failed"),  # First file fails
                    Mock(id="resume_002")  # Second file succeeds
                ]
                mock_resume_service.process_resume.return_value = {
                    "success": True,
                    "sections_found": 3,
                    "skills_found": 8
                }
                
                # Mock file storage
                with patch('app.services.batch_processing_service.file_storage') as mock_storage:
                    mock_storage.upload_file.return_value = True
                    
                    # Act
                    result = await batch_service.process_batch_upload(
                        sample_files_data, 
                        None, 
                        max_concurrent=2
                    )
                    
                    # Assert
                    assert result is not None
                    assert result["status"] == "completed"
                    assert result["total_files"] == 2
                    assert result["successful"] == 1
                    assert result["failed"] == 1
                    assert len(result["results"]) == 2
    
    @pytest.mark.asyncio
    async def test_process_batch_upload_vacancy_not_found(self, batch_service, mock_db, sample_files_data):
        """Test batch upload with non-existent vacancy"""
        # Arrange
        vacancy_id = "nonexistent_vacancy"
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        # Act & Assert
        with pytest.raises(Exception, match="Vacancy with ID nonexistent_vacancy not found"):
            await batch_service.process_batch_upload(sample_files_data, vacancy_id)
    
    def test_get_batch_status_success(self, batch_service):
        """Test successful batch status retrieval"""
        # Arrange
        batch_id = "test_batch_001"
        expected_status = {
            "batch_id": batch_id,
            "status": "completed",
            "total_files": 2,
            "successful": 2,
            "failed": 0
        }
        
        # Mock cache service
        with patch('app.services.batch_processing_service.cache_service') as mock_cache:
            mock_cache.get.return_value = expected_status
            
            # Act
            result = batch_service.get_batch_status(batch_id)
            
            # Assert
            assert result == expected_status
            mock_cache.get.assert_called_once_with("batch_processing", batch_id)
    
    def test_get_batch_status_not_found(self, batch_service):
        """Test batch status retrieval when not found"""
        # Arrange
        batch_id = "nonexistent_batch"
        
        # Mock cache service
        with patch('app.services.batch_processing_service.cache_service') as mock_cache:
            mock_cache.get.return_value = None
            
            # Act
            result = batch_service.get_batch_status(batch_id)
            
            # Assert
            assert result is None
    
    def test_get_batch_statistics(self, batch_service):
        """Test batch statistics retrieval"""
        # Act
        result = batch_service.get_batch_statistics()
        
        # Assert
        assert result is not None
        assert "total_batches" in result
        assert "successful_batches" in result
        assert "failed_batches" in result
        assert "average_processing_time" in result
        assert "total_files_processed" in result
    
    @pytest.mark.asyncio
    async def test_process_single_file_success(self, batch_service, sample_files_data):
        """Test successful single file processing within batch"""
        # Arrange
        file_data = sample_files_data[0]
        batch_id = "test_batch_001"
        file_index = 0
        
        # Mock resume service
        with patch.object(batch_service, 'resume_service') as mock_resume_service:
            mock_resume_service.create_resume.return_value = Mock(id="resume_001")
            mock_resume_service.process_resume.return_value = {
                "success": True,
                "sections_found": 5,
                "skills_found": 10
            }
            
            # Mock file storage
            with patch('app.services.batch_processing_service.file_storage') as mock_storage:
                mock_storage.upload_file.return_value = True
                
                # Create semaphore
                import asyncio
                semaphore = asyncio.Semaphore(1)
                
                # Act
                result = await batch_service._process_single_file(
                    file_data, 
                    "test_vacancy_001", 
                    batch_id, 
                    file_index, 
                    semaphore
                )
                
                # Assert
                assert result is not None
                assert result["filename"] == file_data["filename"]
                assert result["resume_id"] == "resume_001"
                assert result["sections_found"] == 5
                assert result["skills_found"] == 10
    
    @pytest.mark.asyncio
    async def test_process_single_file_missing_data(self, batch_service):
        """Test single file processing with missing data"""
        # Arrange
        file_data = {"filename": "test.pdf"}  # Missing content
        batch_id = "test_batch_001"
        file_index = 0
        
        # Create semaphore
        import asyncio
        semaphore = asyncio.Semaphore(1)
        
        # Act & Assert
        with pytest.raises(Exception, match="Missing filename or content"):
            await batch_service._process_single_file(
                file_data, 
                None, 
                batch_id, 
                file_index, 
                semaphore
            )
    
    @pytest.mark.asyncio
    async def test_process_single_file_upload_failure(self, batch_service, sample_files_data):
        """Test single file processing when upload fails"""
        # Arrange
        file_data = sample_files_data[0]
        batch_id = "test_batch_001"
        file_index = 0
        
        # Mock file storage to fail
        with patch('app.services.batch_processing_service.file_storage') as mock_storage:
            mock_storage.upload_file.return_value = False
            
            # Create semaphore
            import asyncio
            semaphore = asyncio.Semaphore(1)
            
            # Act & Assert
            with pytest.raises(Exception, match="Failed to upload file to storage"):
                await batch_service._process_single_file(
                    file_data, 
                    None, 
                    batch_id, 
                    file_index, 
                    semaphore
                )
