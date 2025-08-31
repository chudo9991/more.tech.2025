from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.interview_code_service import InterviewCodeService
from app.schemas.interview_code import (
    InterviewCodeResponse,
    InterviewCodeValidation,
    InterviewCodeValidationResponse
)
from typing import List

router = APIRouter()


@router.post("/generate/{resume_id}", response_model=InterviewCodeResponse)
async def generate_interview_code(
    resume_id: str,
    db: Session = Depends(get_db)
) -> InterviewCodeResponse:
    """Generate a unique 6-digit code for resume interview"""
    try:
        code_service = InterviewCodeService(db)
        interview_code = code_service.generate_code(resume_id)
        
        if not interview_code:
            raise HTTPException(status_code=404, detail="Resume not found or failed to generate code")
        
        return InterviewCodeResponse.from_orm(interview_code)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/validate", response_model=InterviewCodeValidationResponse)
async def validate_interview_code(
    code_data: InterviewCodeValidation,
    db: Session = Depends(get_db)
) -> InterviewCodeValidationResponse:
    """Validate interview code and return resume_id if valid"""
    try:
        code_service = InterviewCodeService(db)
        interview_code = code_service.validate_code(code_data.code)
        
        if interview_code:
            return InterviewCodeValidationResponse(
                valid=True,
                resume_id=interview_code.resume_id,
                message="Code validated successfully"
            )
        else:
            return InterviewCodeValidationResponse(
                valid=False,
                message="Invalid or already used code"
            )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/resume/{resume_id}", response_model=List[InterviewCodeResponse])
async def get_resume_codes(
    resume_id: str,
    db: Session = Depends(get_db)
) -> List[InterviewCodeResponse]:
    """Get all codes for a specific resume"""
    try:
        code_service = InterviewCodeService(db)
        codes = code_service.get_codes_by_resume(resume_id)
        
        return [InterviewCodeResponse.from_orm(code) for code in codes]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{code_id}")
async def delete_interview_code(
    code_id: str,
    db: Session = Depends(get_db)
):
    """Delete interview code"""
    try:
        code_service = InterviewCodeService(db)
        success = code_service.delete_code(code_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Code not found")
        
        return {"message": "Code deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
