from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import uuid


class InterviewCode(Base):
    __tablename__ = "interview_codes"
    
    id = Column(String, primary_key=True, default=lambda: f"CODE_{uuid.uuid4().hex[:8].upper()}")
    code = Column(String(6), unique=True, nullable=False, index=True)
    resume_id = Column(String, ForeignKey("resumes.id"), nullable=False)
    is_used = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    used_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    resume = relationship("Resume", back_populates="interview_codes")
    
    def __repr__(self):
        return f"<InterviewCode(id={self.id}, code={self.code}, resume_id={self.resume_id}, is_used={self.is_used})>"
