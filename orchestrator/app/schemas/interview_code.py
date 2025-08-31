from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class InterviewCodeBase(BaseModel):
    code: str
    resume_id: str


class InterviewCodeCreate(InterviewCodeBase):
    pass


class InterviewCodeResponse(InterviewCodeBase):
    id: str
    is_used: bool
    created_at: datetime
    used_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class InterviewCodeValidation(BaseModel):
    code: str


class InterviewCodeValidationResponse(BaseModel):
    valid: bool
    resume_id: Optional[str] = None
    message: str
