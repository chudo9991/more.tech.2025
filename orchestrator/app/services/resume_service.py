"""
Resume service for managing resume data and operations
"""
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session as DBSession
from sqlalchemy import and_, desc, func
from datetime import datetime
import uuid

from app.models import Resume, ResumeBlock, ResumeSkill, Vacancy
from app.schemas.resume import ResumeCreate, ResumeUpdate, ResumeListResponse, ResumeResponse
from app.utils.file_storage import file_storage
from app.services.text_extraction_service import text_extractor
from app.services.resume_parser_service import resume_parser
from app.services.relevance_scoring_service import relevance_scorer
from app.services.cache_service import cache_service


class ResumeService:
    def __init__(self, db: DBSession):
        self.db = db

    def create_resume(self, resume_data: ResumeCreate) -> Resume:
        """Create a new resume record"""
        resume_id = f"RESUME_{uuid.uuid4().hex[:8].upper()}"
        
        resume = Resume(
            id=resume_id,
            vacancy_id=resume_data.vacancy_id,
            vacancy_code=resume_data.vacancy_code,
            filename=resume_data.filename,
            original_filename=resume_data.original_filename,
            file_size=resume_data.file_size,
            file_type=resume_data.file_type,
            status=resume_data.status,
            total_score=resume_data.total_score,
            confidence_score=resume_data.confidence_score,
            processing_errors=resume_data.processing_errors
        )
        
        self.db.add(resume)
        self.db.commit()
        self.db.refresh(resume)
        return resume

    def get_resume(self, resume_id: str) -> Optional[Resume]:
        """Get resume by ID"""
        return self.db.query(Resume).filter(Resume.id == resume_id).first()

    def get_resumes(
        self, 
        skip: int = 0, 
        limit: int = 25,
        vacancy_id: Optional[str] = None,
        status: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get list of resumes with filters and pagination"""
        query = self.db.query(Resume)
        
        if vacancy_id:
            query = query.filter(Resume.vacancy_id == vacancy_id)
        
        if status:
            query = query.filter(Resume.status == status)
        
        # Get total count for pagination
        total = query.count()
        
        # Get resumes with pagination
        resumes = query.order_by(desc(Resume.created_at)).offset(skip).limit(limit).all()
        
        # Get vacancy titles
        vacancy_ids = list(set([r.vacancy_id for r in resumes if r.vacancy_id]))
        vacancies = {}
        if vacancy_ids:
            vacancy_models = self.db.query(Vacancy).filter(Vacancy.id.in_(vacancy_ids)).all()
            vacancies = {v.id: {'title': v.title, 'code': v.vacancy_code} for v in vacancy_models}
        
        # Convert to response format
        resume_list = []
        for resume in resumes:
            resume_data = ResumeListResponse.from_orm(resume)
            vacancy_info = vacancies.get(resume.vacancy_id, {})
            resume_data.vacancy_title = vacancy_info.get('title')
            resume_list.append(resume_data)
        
        # Calculate pagination info
        page = (skip // limit) + 1
        total_pages = (total + limit - 1) // limit
        
        return {
            "resumes": resume_list,
            "total": total,
            "page": page,
            "size": limit,
            "total_pages": total_pages
        }

    def update_resume(self, resume_id: str, resume_data: ResumeUpdate) -> Optional[Resume]:
        """Update resume record"""
        resume = self.get_resume(resume_id)
        if not resume:
            return None
        
        update_data = resume_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(resume, field, value)
        
        resume.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(resume)
        return resume

    def delete_resume(self, resume_id: str) -> bool:
        """Delete resume record and associated file"""
        resume = self.get_resume(resume_id)
        if not resume:
            return False
        
        # Delete file from MinIO
        if resume.filename:
            file_storage.delete_file(resume.filename)
        
        self.db.delete(resume)
        self.db.commit()
        return True

    def get_resume_detail(self, resume_id: str) -> Optional[ResumeResponse]:
        """Get detailed resume information with blocks and skills"""
        resume = self.db.query(Resume).filter(Resume.id == resume_id).first()
        if not resume:
            return None
        
        # Get vacancy title
        vacancy_title = None
        if resume.vacancy_id:
            vacancy = self.db.query(Vacancy).filter(Vacancy.id == resume.vacancy_id).first()
            if vacancy:
                vacancy_title = vacancy.title
        
        resume_data = ResumeResponse.from_orm(resume)
        resume_data.vacancy_title = vacancy_title
        
        return resume_data

    def get_resume_statistics(self) -> Dict[str, Any]:
        """Get resume statistics with caching"""
        # Try to get from cache first
        cached_stats = cache_service.get_statistics("resume_overview")
        if cached_stats:
            return cached_stats
        
        total_resumes = self.db.query(Resume).count()
        processed_resumes = self.db.query(Resume).filter(Resume.status == "analyzed").count()
        error_resumes = self.db.query(Resume).filter(Resume.status == "error").count()
        
        # Calculate average score
        resumes_with_score = self.db.query(Resume).filter(
            and_(
                Resume.status == "analyzed",
                Resume.total_score.isnot(None)
            )
        ).all()
        
        average_score = 0.0
        if resumes_with_score:
            total_score = sum(float(r.total_score) for r in resumes_with_score)
            average_score = total_score / len(resumes_with_score)
        
        # Score distribution
        score_distribution = {
            "excellent": self.db.query(Resume).filter(
                and_(Resume.total_score >= 80, Resume.status == "analyzed")
            ).count(),
            "good": self.db.query(Resume).filter(
                and_(Resume.total_score >= 60, Resume.total_score < 80, Resume.status == "analyzed")
            ).count(),
            "average": self.db.query(Resume).filter(
                and_(Resume.total_score >= 40, Resume.total_score < 60, Resume.status == "analyzed")
            ).count(),
            "poor": self.db.query(Resume).filter(
                and_(Resume.total_score < 40, Resume.status == "analyzed")
            ).count()
        }
        
        # Top vacancies by resume count
        top_vacancies = self.db.query(
            Resume.vacancy_id,
            Resume.vacancy_code,
            func.count(Resume.id).label('count')
        ).filter(Resume.vacancy_id.isnot(None)).group_by(
            Resume.vacancy_id, Resume.vacancy_code
        ).order_by(desc('count')).limit(5).all()
        
        top_vacancies_data = []
        for vacancy_id, vacancy_code, count in top_vacancies:
            vacancy = self.db.query(Vacancy).filter(Vacancy.id == vacancy_id).first()
            top_vacancies_data.append({
                "vacancy_id": vacancy_id,
                "vacancy_code": vacancy_code,
                "title": vacancy.title if vacancy else "Unknown",
                "count": count
            })
        
        stats = {
            "total_resumes": total_resumes,
            "processed_resumes": processed_resumes,
            "error_resumes": error_resumes,
            "average_score": round(average_score, 2),
            "score_distribution": score_distribution,
            "top_vacancies": top_vacancies_data
        }
        
        # Cache the statistics
        cache_service.set_statistics("resume_overview", stats)
        
        return stats
    
    async def process_resume(self, resume_id: str) -> Dict[str, Any]:
        """Process resume file and extract structured data"""
        try:
            resume = self.get_resume(resume_id)
            if not resume:
                raise Exception("Resume not found")
            
            # Update status to processing
            resume.status = "processing"
            self.db.commit()
            
            # Download file from MinIO
            file_data = file_storage.download_file(resume.filename)
            if not file_data:
                raise Exception("File not found in storage")
            
            # Read file content
            file_content = file_data.read()
            
            # Extract text from file
            extraction_result = text_extractor.extract_text(file_content, resume.file_type)
            if not extraction_result["success"]:
                raise Exception(f"Text extraction failed: {extraction_result['error']}")
            
            # Parse resume text
            parsing_result = resume_parser.parse_resume(extraction_result["text"])
            if not parsing_result["success"]:
                raise Exception(f"Resume parsing failed: {parsing_result['error']}")
            
            # Create resume blocks
            self._create_resume_blocks(resume, parsing_result["sections"])
            
            # Create resume skills
            self._create_resume_skills(resume, parsing_result["skills"])
            
            # Update resume with extracted data
            resume.status = "analyzed"
            resume.total_score = 0  # Will be calculated later
            resume.confidence_score = parsing_result["summary"]["total_skills"] / 10  # Simple confidence based on skills found
            
            self.db.commit()
            
            # Calculate relevance score if vacancy is specified
            if resume.vacancy_id:
                await self._calculate_relevance_score(resume)
            
            # Invalidate cache for this resume
            cache_service.invalidate_resume_cache(resume.id)
            
            return {
                "success": True,
                "resume_id": resume.id,
                "sections_found": parsing_result["summary"]["total_sections"],
                "skills_found": parsing_result["summary"]["total_skills"],
                "experience_years": parsing_result["summary"]["experience_years"],
                "education_level": parsing_result["summary"]["education_level"]
            }
            
        except Exception as e:
            # Update resume with error
            if resume:
                resume.status = "error"
                resume.processing_errors = str(e)
                self.db.commit()
            
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _calculate_relevance_score(self, resume: Resume):
        """Calculate relevance score for resume"""
        try:
            # Get vacancy
            vacancy = self.db.query(Vacancy).filter(Vacancy.id == resume.vacancy_id).first()
            if not vacancy:
                return
            
            # Calculate score
            scoring_result = await relevance_scorer.calculate_resume_score(resume, vacancy)
            
            if scoring_result["success"]:
                # Update resume with scores
                resume.total_score = scoring_result["total_score"]
                resume.confidence_score = scoring_result["confidence_score"]
                
                # Update resume blocks with relevance scores
                component_scores = scoring_result["component_scores"]
                for block in resume.resume_blocks:
                    if block.block_type in component_scores:
                        block.relevance_score = component_scores[block.block_type]["score"]
                        block.analysis_notes = str(component_scores[block.block_type]["details"])
                
                self.db.commit()
                
        except Exception as e:
            print(f"Error calculating relevance score: {str(e)}")
    
    async def calculate_resume_score(self, resume_id: str) -> Dict[str, Any]:
        """Calculate relevance score for resume with caching"""
        try:
            # Try to get from cache first
            cached_score = cache_service.get_resume_score(resume_id)
            if cached_score:
                return {
                    "success": True,
                    "resume_id": resume_id,
                    "total_score": cached_score.get("total_score"),
                    "confidence_score": cached_score.get("confidence_score"),
                    "cached": True
                }
            
            resume = self.get_resume(resume_id)
            if not resume:
                raise Exception("Resume not found")
            
            if not resume.vacancy_id:
                raise Exception("Resume not linked to vacancy")
            
            await self._calculate_relevance_score(resume)
            
            # Cache the score
            score_data = {
                "total_score": resume.total_score,
                "confidence_score": resume.confidence_score
            }
            cache_service.set_resume_score(resume_id, score_data)
            
            return {
                "success": True,
                "resume_id": resume.id,
                "total_score": resume.total_score,
                "confidence_score": resume.confidence_score,
                "cached": False
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _create_resume_blocks(self, resume: Resume, sections: Dict[str, str]):
        """Create resume blocks from parsed sections"""
        for section_name, section_text in sections.items():
            if section_text.strip():
                block = ResumeBlock(
                    id=f"BLOCK_{uuid.uuid4().hex[:8].upper()}",
                    resume_id=resume.id,
                    block_type=section_name,
                    block_name=section_name.replace('_', ' ').title(),
                    extracted_text=section_text[:1000],  # Limit text length
                    relevance_score=50.0,  # Default score
                    confidence_score=80.0  # Default confidence
                )
                self.db.add(block)
    
    def _create_resume_skills(self, resume: Resume, skills: List[Dict[str, Any]]):
        """Create resume skills from parsed skills"""
        for skill_data in skills:
            skill = ResumeSkill(
                id=f"SKILL_{uuid.uuid4().hex[:8].upper()}",
                resume_id=resume.id,
                skill_name=skill_data["name"],
                skill_category=skill_data["category"],
                experience_level="intermediate",  # Default level
                confidence_score=skill_data.get("confidence", 80.0),
                extracted_from=skill_data.get("context", "")[:500]  # Limit context length
            )
            self.db.add(skill)
