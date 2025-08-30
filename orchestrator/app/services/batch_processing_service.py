"""
Batch processing service for multiple resume files
"""
import asyncio
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from app.models import Resume, Vacancy
from app.schemas.resume import ResumeCreate
from app.services.resume_service import ResumeService
from app.services.cache_service import cache_service
from app.utils.file_storage import file_storage


class BatchProcessingService:
    """Service for processing multiple resume files in batch"""
    
    def __init__(self, db: Session):
        self.db = db
        self.resume_service = ResumeService(db)
    
    async def process_batch_upload(
        self, 
        files: List[Dict[str, Any]], 
        vacancy_id: Optional[str] = None,
        max_concurrent: int = 3
    ) -> Dict[str, Any]:
        """Process multiple resume files in batch"""
        try:
            batch_id = str(uuid.uuid4())
            start_time = datetime.now()
            
            # Validate vacancy if provided
            if vacancy_id:
                vacancy = self.db.query(Vacancy).filter(Vacancy.id == vacancy_id).first()
                if not vacancy:
                    raise Exception(f"Vacancy with ID {vacancy_id} not found")
            
            # Create batch processing record
            batch_info = {
                "batch_id": batch_id,
                "total_files": len(files),
                "start_time": start_time.isoformat(),
                "status": "processing",
                "results": []
            }
            
            # Store batch info in cache
            cache_service.set("batch_processing", batch_id, batch_info, ttl=3600)
            
            # Process files with concurrency limit
            semaphore = asyncio.Semaphore(max_concurrent)
            tasks = []
            
            for i, file_data in enumerate(files):
                task = asyncio.create_task(
                    self._process_single_file(
                        file_data, 
                        vacancy_id, 
                        batch_id, 
                        i, 
                        semaphore
                    )
                )
                tasks.append(task)
            
            # Wait for all tasks to complete
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results
            successful = 0
            failed = 0
            processed_results = []
            
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    failed += 1
                    processed_results.append({
                        "file_index": i,
                        "filename": files[i].get("filename", f"file_{i}"),
                        "status": "error",
                        "error": str(result)
                    })
                else:
                    successful += 1
                    processed_results.append({
                        "file_index": i,
                        "filename": result.get("filename"),
                        "status": "success",
                        "resume_id": result.get("resume_id"),
                        "sections_found": result.get("sections_found"),
                        "skills_found": result.get("skills_found")
                    })
            
            # Update batch info
            end_time = datetime.now()
            processing_time = (end_time - start_time).total_seconds()
            
            batch_info.update({
                "status": "completed",
                "end_time": end_time.isoformat(),
                "processing_time_seconds": processing_time,
                "successful": successful,
                "failed": failed,
                "results": processed_results
            })
            
            # Update cache
            cache_service.set("batch_processing", batch_id, batch_info, ttl=3600)
            
            # Invalidate relevant caches
            cache_service.clear_prefix("statistics")
            if vacancy_id:
                cache_service.invalidate_vacancy_cache(vacancy_id)
            
            return {
                "batch_id": batch_id,
                "status": "completed",
                "total_files": len(files),
                "successful": successful,
                "failed": failed,
                "processing_time_seconds": processing_time,
                "results": processed_results
            }
            
        except Exception as e:
            if 'batch_id' in locals():
                batch_info.update({
                    "status": "error",
                    "error": str(e),
                    "end_time": datetime.now().isoformat()
                })
                cache_service.set("batch_processing", batch_id, batch_info, ttl=3600)
            
            raise Exception(f"Batch processing failed: {str(e)}")
    
    async def _process_single_file(
        self, 
        file_data: Dict[str, Any], 
        vacancy_id: Optional[str], 
        batch_id: str, 
        file_index: int, 
        semaphore: asyncio.Semaphore
    ) -> Dict[str, Any]:
        """Process a single file within batch"""
        async with semaphore:
            try:
                print(f"DEBUG: Starting to process file {file_index}")
                filename = file_data.get("filename")
                file_content = file_data.get("content")
                file_type = file_data.get("file_type", "pdf")
                
                print(f"DEBUG: File data - filename: {filename}, content size: {len(file_content) if file_content else 0}, type: {file_type}")
                
                if not filename or not file_content:
                    raise Exception("Missing filename or content")
                
                # Generate unique filename
                unique_filename = f"{batch_id}_{file_index}_{filename}"
                print(f"DEBUG: Unique filename: {unique_filename}")
                
                # Upload to MinIO
                print(f"DEBUG: Uploading to MinIO...")
                upload_success = file_storage.upload_file(
                    file_content,  # file_data: bytes
                    unique_filename,  # filename: str
                    f"application/{file_type}"  # content_type: str
                )
                
                if not upload_success:
                    raise Exception("Failed to upload file to storage")
                
                print(f"DEBUG: File uploaded successfully to MinIO with name: {upload_success}")
                
                # Create resume record
                resume_data = ResumeCreate(
                    filename=upload_success,  # Use the actual filename from MinIO
                    original_filename=filename,
                    file_type=file_type,
                    file_size=len(file_content),  # Add file size
                    vacancy_id=vacancy_id,
                    status="uploaded"
                )
                
                print(f"DEBUG: Creating resume record...")
                resume = self.resume_service.create_resume(resume_data)
                print(f"DEBUG: Resume created with ID: {resume.id}")
                
                # Process resume
                print(f"DEBUG: Starting resume processing...")
                process_result = await self.resume_service.process_resume(resume.id)
                print(f"DEBUG: Resume processing completed: {process_result}")
                
                return {
                    "filename": filename,
                    "resume_id": resume.id,
                    "sections_found": process_result.get("sections_found"),
                    "skills_found": process_result.get("skills_found")
                }
                
            except Exception as e:
                print(f"DEBUG: Error processing file {file_index}: {str(e)}")
                raise Exception(f"File processing failed: {str(e)}")
    
    def get_batch_status(self, batch_id: str) -> Optional[Dict[str, Any]]:
        """Get batch processing status"""
        try:
            return cache_service.get("batch_processing", batch_id)
        except Exception:
            return None
    
    def get_batch_statistics(self) -> Dict[str, Any]:
        """Get batch processing statistics"""
        return {
            "total_batches": 0,
            "successful_batches": 0,
            "failed_batches": 0,
            "average_processing_time": 0,
            "total_files_processed": 0
        }
