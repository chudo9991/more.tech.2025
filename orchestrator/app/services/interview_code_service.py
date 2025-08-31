import random
import string
from typing import Optional
from sqlalchemy.orm import Session
from app.models.interview_code import InterviewCode
from app.models.resume import Resume
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class InterviewCodeService:
    def __init__(self, db: Session):
        self.db = db
    
    def generate_code(self, resume_id: str) -> Optional[InterviewCode]:
        """Generate a unique 6-digit code for resume interview"""
        try:
            # Check if resume exists
            resume = self.db.query(Resume).filter(Resume.id == resume_id).first()
            if not resume:
                logger.error(f"Resume {resume_id} not found")
                return None
            
            # Generate unique 6-digit code
            max_attempts = 100
            for attempt in range(max_attempts):
                code = ''.join(random.choices(string.digits, k=6))
                
                # Check if code already exists
                existing_code = self.db.query(InterviewCode).filter(InterviewCode.code == code).first()
                if not existing_code:
                    break
            else:
                logger.error("Failed to generate unique code after 100 attempts")
                return None
            
            # Create interview code
            interview_code = InterviewCode(
                code=code,
                resume_id=resume_id
            )
            
            self.db.add(interview_code)
            self.db.commit()
            self.db.refresh(interview_code)
            
            logger.info(f"Generated interview code {code} for resume {resume_id}")
            return interview_code
            
        except Exception as e:
            logger.error(f"Error generating interview code: {str(e)}")
            self.db.rollback()
            return None
    
    def validate_code(self, code: str) -> Optional[InterviewCode]:
        """Validate interview code and mark as used"""
        try:
            # Find code
            interview_code = self.db.query(InterviewCode).filter(
                InterviewCode.code == code,
                InterviewCode.is_used == False
            ).first()
            
            if not interview_code:
                logger.warning(f"Invalid or used code: {code}")
                return None
            
            # Mark as used
            interview_code.is_used = True
            interview_code.used_at = datetime.utcnow()
            
            self.db.commit()
            self.db.refresh(interview_code)
            
            logger.info(f"Code {code} validated and marked as used")
            return interview_code
            
        except Exception as e:
            logger.error(f"Error validating code: {str(e)}")
            self.db.rollback()
            return None
    
    def get_codes_by_resume(self, resume_id: str) -> list[InterviewCode]:
        """Get all codes for a specific resume"""
        return self.db.query(InterviewCode).filter(
            InterviewCode.resume_id == resume_id
        ).order_by(InterviewCode.created_at.desc()).all()
    
    def delete_code(self, code_id: str) -> bool:
        """Delete interview code"""
        try:
            code = self.db.query(InterviewCode).filter(InterviewCode.id == code_id).first()
            if code:
                self.db.delete(code)
                self.db.commit()
                logger.info(f"Deleted interview code {code_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting code: {str(e)}")
            self.db.rollback()
            return False
