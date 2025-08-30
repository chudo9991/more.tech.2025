"""
Batch processing API endpoints
"""
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.batch_processing_service import BatchProcessingService
from app.schemas.resume import BatchUploadRequest, BatchUploadResponse

router = APIRouter()


@router.post("/upload", response_model=BatchUploadResponse)
async def batch_upload_resumes(
    files: List[UploadFile] = File(...),
    vacancy_id: Optional[str] = Form(None),
    max_concurrent: int = Form(3),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Upload and process multiple resume files in batch"""
    try:
        if not files:
            raise HTTPException(status_code=400, detail="No files provided")
        
        if len(files) > 50:
            raise HTTPException(status_code=400, detail="Maximum 50 files allowed per batch")
        
        # Prepare file data
        file_data_list = []
        for file in files:
            if file.size and file.size > 10 * 1024 * 1024:  # 10MB limit
                raise HTTPException(
                    status_code=400, 
                    detail=f"File {file.filename} is too large (max 10MB)"
                )
            
            content = await file.read()
            file_type = file.filename.split('.')[-1].lower() if '.' in file.filename else 'pdf'
            
            file_data_list.append({
                "filename": file.filename,
                "content": content,
                "file_type": file_type
            })
        
        # Process batch
        batch_service = BatchProcessingService(db)
        result = await batch_service.process_batch_upload(
            file_data_list, 
            vacancy_id, 
            max_concurrent
        )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status/{batch_id}")
async def get_batch_status(
    batch_id: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get batch processing status"""
    try:
        batch_service = BatchProcessingService(db)
        status = batch_service.get_batch_status(batch_id)
        
        if not status:
            raise HTTPException(status_code=404, detail="Batch not found")
        
        return status
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/statistics")
async def get_batch_statistics(
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get batch processing statistics"""
    try:
        batch_service = BatchProcessingService(db)
        return batch_service.get_batch_statistics()
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload/json")
async def batch_upload_resumes_json(
    request: BatchUploadRequest,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Upload and process multiple resume files using JSON payload"""
    try:
        if not request.files:
            raise HTTPException(status_code=400, detail="No files provided")
        
        if len(request.files) > 50:
            raise HTTPException(status_code=400, detail="Maximum 50 files allowed per batch")
        
        # Process batch
        batch_service = BatchProcessingService(db)
        result = await batch_service.process_batch_upload(
            request.files, 
            request.vacancy_id, 
            request.max_concurrent or 3
        )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
