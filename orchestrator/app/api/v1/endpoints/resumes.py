"""
Resume API endpoints
"""
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Depends, Query, UploadFile, File, Form
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.resume import (
    ResumeCreate, ResumeUpdate, ResumeResponse, ResumeListResponse,
    ResumeStatisticsResponse
)
from app.services.resume_service import ResumeService
from app.utils.file_storage import file_storage

router = APIRouter()


@router.get("/")
async def get_resumes(
    skip: int = Query(0, ge=0),
    limit: int = Query(25, ge=1, le=100),
    vacancy_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get list of resumes with filters and pagination"""
    try:
        resume_service = ResumeService(db)
        result = resume_service.get_resumes(skip, limit, vacancy_id, status)
        
        # Возвращаем результат напрямую
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/statistics", response_model=ResumeStatisticsResponse)
async def get_resume_statistics(
    db: Session = Depends(get_db)
) -> ResumeStatisticsResponse:
    """Get resume statistics"""
    try:
        resume_service = ResumeService(db)
        statistics = resume_service.get_resume_statistics()
        return ResumeStatisticsResponse(**statistics)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{resume_id}", response_model=ResumeResponse)
async def get_resume(
    resume_id: str,
    db: Session = Depends(get_db)
) -> ResumeResponse:
    """Get detailed resume information"""
    try:
        resume_service = ResumeService(db)
        resume = resume_service.get_resume_detail(resume_id)
        if not resume:
            raise HTTPException(status_code=404, detail="Resume not found")
        return resume
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/", response_model=ResumeResponse)
async def create_resume(
    resume_data: ResumeCreate,
    db: Session = Depends(get_db)
) -> ResumeResponse:
    """Create a new resume record"""
    try:
        resume_service = ResumeService(db)
        resume = resume_service.create_resume(resume_data)
        return ResumeResponse.from_orm(resume)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{resume_id}", response_model=ResumeResponse)
async def update_resume(
    resume_id: str,
    resume_data: ResumeUpdate,
    db: Session = Depends(get_db)
) -> ResumeResponse:
    """Update resume record"""
    try:
        resume_service = ResumeService(db)
        resume = resume_service.update_resume(resume_id, resume_data)
        if not resume:
            raise HTTPException(status_code=404, detail="Resume not found")
        return ResumeResponse.from_orm(resume)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{resume_id}")
async def delete_resume(
    resume_id: str,
    db: Session = Depends(get_db)
) -> Dict[str, str]:
    """Delete resume record"""
    try:
        resume_service = ResumeService(db)
        success = resume_service.delete_resume(resume_id)
        if not success:
            raise HTTPException(status_code=404, detail="Resume not found")
        return {"message": "Resume deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{resume_id}/download")
async def download_resume_file(
    resume_id: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get download URL for resume file"""
    try:
        resume_service = ResumeService(db)
        resume = resume_service.get_resume(resume_id)
        if not resume:
            raise HTTPException(status_code=404, detail="Resume not found")
        
        # Generate presigned URL for download
        download_url = file_storage.get_file_url(resume.filename)
        
        return {
            "download_url": download_url,
            "filename": resume.original_filename,
            "expires_in": 3600  # 1 hour
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{resume_id}/process")
async def process_resume(
    resume_id: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Process resume file and extract structured data"""
    try:
        resume_service = ResumeService(db)
        result = await resume_service.process_resume(resume_id)
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{resume_id}/calculate-score")
async def calculate_resume_score(
    resume_id: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Calculate relevance score for resume"""
    try:
        resume_service = ResumeService(db)
        result = await resume_service.calculate_resume_score(resume_id)
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    vacancy_id: Optional[str] = Form(None),
    vacancy_code: Optional[str] = Form(None),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Upload resume file to MinIO and create database record"""
    try:
        # Validate file type
        allowed_types = ["pdf", "docx", "rtf", "txt"]
        file_extension = file.filename.split(".")[-1].lower() if "." in file.filename else ""
        
        if file_extension not in allowed_types:
            raise HTTPException(
                status_code=400, 
                detail=f"File type not supported. Allowed types: {', '.join(allowed_types)}"
            )
        
        # Validate file size (max 10MB)
        if file.size and file.size > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File size too large. Maximum 10MB allowed.")
        
        # Upload file to MinIO
        file_content = await file.read()
        storage_filename = file_storage.upload_file(
            file_data=file_content,
            filename=file.filename,
            content_type=file.content_type or "application/octet-stream"
        )
        
        # Create resume record in database
        resume_service = ResumeService(db)
        resume_data = ResumeCreate(
            vacancy_id=vacancy_id,
            vacancy_code=vacancy_code,
            filename=storage_filename,
            original_filename=file.filename,
            file_size=file.size or 0,
            file_type=file_extension,
            status="uploaded"
        )
        
        resume = resume_service.create_resume(resume_data)
        
        return {
            "message": "Resume uploaded successfully",
            "resume_id": resume.id,
            "filename": storage_filename,
            "original_filename": file.filename,
            "file_size": file.size,
            "file_type": file_extension,
            "status": resume.status
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
