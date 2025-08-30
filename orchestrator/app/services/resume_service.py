"""
Resume service for managing resume data and operations
"""
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session as DBSession
from sqlalchemy import and_, desc, func
from datetime import datetime
import uuid
import logging

from app.models import Resume, ResumeBlock, ResumeSkill, Vacancy, VacancySectionKeywords
from app.schemas.resume import ResumeCreate, ResumeUpdate, ResumeListResponse, ResumeResponse
from app.schemas.vacancy_skills import ResumeSkillsAnalysisResponse
from app.utils.file_storage import file_storage
from app.services.text_extraction_service import text_extractor
from app.services.resume_parser_service import resume_parser
from app.services.relevance_scoring_service import relevance_scorer
from app.services.cache_service import cache_service
from app.services.vacancy_skills_extractor import vacancy_skills_extractor

logger = logging.getLogger(__name__)


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
            
            # Get vacancy requirements for context-aware parsing
            vacancy_requirements = {}
            if resume.vacancy_id:
                vacancy = self.db.query(Vacancy).filter(Vacancy.id == resume.vacancy_id).first()
                if vacancy:
                    vacancy_requirements = {
                        'responsibilities': vacancy.responsibilities or '',
                        'requirements': vacancy.requirements or '',
                        'programs': vacancy.special_programs or '',
                        'additional': vacancy.additional_info or ''
                    }
            
            # Parse resume text with vacancy context
            logger.info(f"Parsing resume text with length: {len(extraction_result['text'])}")
            logger.info(f"Vacancy requirements: {list(vacancy_requirements.keys())}")
            
            parsing_result = await resume_parser.parse_resume(
                extraction_result["text"], 
                vacancy_requirements
            )
            if not parsing_result["success"]:
                raise Exception(f"Resume parsing failed: {parsing_result['error']}")
            
            logger.info(f"Parsing result: {parsing_result['summary']}")
            logger.info(f"Found sections: {list(parsing_result['sections'].keys())}")
            
            # Create resume blocks
            self._create_resume_blocks(resume, parsing_result["sections"])
            
            # Create resume skills
            self._create_resume_skills(resume, parsing_result["skills"])
            
            # Update resume with extracted data
            resume.status = "analyzed"
            resume.total_score = 0  # Will be calculated later
            # Calculate confidence based on skills found (0-100 scale)
            total_skills = parsing_result["summary"]["total_skills"]
            resume.confidence_score = min(total_skills * 2, 100.0)  # Max 2 points per skill, capped at 100%
            
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
                        component_score = component_scores[block.block_type]
                        block.relevance_score = component_score["score"]
                        block.confidence_score = component_score.get("confidence", 0)  # Добавили confidence
                        
                        # Convert details to human-readable text and extract keywords
                        details = component_score["details"]
                        if isinstance(details, dict):
                            # Get analysis_text from LLM response
                            analysis_text = details.get("analysis_text", str(details))
                            # Get extracted_keywords for comparison
                            extracted_keywords = details.get("extracted_keywords", [])
                        else:
                            analysis_text = str(details)
                            extracted_keywords = []
                        
                        block.analysis_notes = analysis_text
                        block.extracted_keywords = extracted_keywords
                
                self.db.commit()
                
        except Exception as e:
            logger.error(f"Error calculating relevance score: {str(e)}")
    
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
    
    async def analyze_resume_with_dynamic_skills(
        self, 
        resume_id: str, 
        vacancy_id: str,
        force_reload: bool = False
    ) -> ResumeSkillsAnalysisResponse:
        """
        Analyze resume using dynamic skills from VacancySkillsExtractor
        
        Args:
            resume_id: ID of the resume to analyze
            vacancy_id: ID of the vacancy
            force_reload: Force reload skills from LLM
            
        Returns:
            ResumeSkillsAnalysisResponse with detailed analysis
        """
        try:
            logger.info(f"Starting analysis for resume {resume_id} and vacancy {vacancy_id}")
            
            # Get resume
            resume = self.get_resume(resume_id)
            if not resume:
                logger.warning(f"Resume {resume_id} not found")
                return ResumeSkillsAnalysisResponse(
                    success=False,
                    resume_id=resume_id,
                    vacancy_id=vacancy_id,
                    skill_matches=[],
                    overall_score=0.0,
                    mandatory_skills_covered=0,
                    total_mandatory_skills=0,
                    analysis_time=0.0,
                    strengths=[],
                    weaknesses=[],
                    recommendations=[],
                    error="Resume not found"
                )
            
            logger.info(f"Found resume: {resume.id}, status: {resume.status}")
            
            # Get vacancy
            vacancy = self.db.query(Vacancy).filter(Vacancy.id == vacancy_id).first()
            if not vacancy:
                logger.warning(f"Vacancy {vacancy_id} not found")
                return ResumeSkillsAnalysisResponse(
                    success=False,
                    resume_id=resume_id,
                    vacancy_id=vacancy_id,
                    skill_matches=[],
                    overall_score=0.0,
                    mandatory_skills_covered=0,
                    total_mandatory_skills=0,
                    analysis_time=0.0,
                    strengths=[],
                    weaknesses=[],
                    recommendations=[],
                    error="Vacancy not found"
                )
            
            logger.info(f"Found vacancy: {vacancy.id}, title: {vacancy.title}")
            
            # Extract skills from vacancy
            logger.info("Extracting skills from vacancy...")
            skills_result = await vacancy_skills_extractor.extract_skills_from_vacancy(
                vacancy=vacancy,
                force_reload=force_reload
            )
            
            if not skills_result.success:
                logger.warning(f"Failed to extract skills: {skills_result.error}")
                return ResumeSkillsAnalysisResponse(
                    success=False,
                    resume_id=resume_id,
                    vacancy_id=vacancy_id,
                    skill_matches=[],
                    overall_score=0.0,
                    mandatory_skills_covered=0,
                    total_mandatory_skills=0,
                    analysis_time=0.0,
                    strengths=[],
                    weaknesses=[],
                    recommendations=[],
                    error="Failed to extract skills from vacancy"
                )
            
            logger.info(f"Extracted {len(skills_result.skills)} skills from vacancy")
            
            # Analyze resume with dynamic skills
            logger.info("Analyzing resume with dynamic skills...")
            analysis_result = await relevance_scorer.calculate_resume_score_with_dynamic_skills(
                resume=resume,
                vacancy=vacancy,
                vacancy_skills=skills_result.skills
            )
            
            logger.info(f"Analysis result success: {analysis_result.get('success')}")
            if not analysis_result["success"]:
                logger.warning(f"Analysis failed: {analysis_result.get('error')}")
                return ResumeSkillsAnalysisResponse(
                    success=False,
                    resume_id=resume_id,
                    vacancy_id=vacancy_id,
                    skill_matches=[],
                    overall_score=0.0,
                    mandatory_skills_covered=0,
                    total_mandatory_skills=0,
                    analysis_time=0.0,
                    strengths=[],
                    weaknesses=[],
                    recommendations=[],
                    error="Failed to analyze resume"
                )
            
            # Extract skills analysis from the result
            skills_analysis = analysis_result.get("skills_analysis")
            if skills_analysis:
                logger.info("Skills analysis found in result")
                return ResumeSkillsAnalysisResponse(
                    success=True,
                    resume_id=resume_id,
                    vacancy_id=vacancy_id,
                    skill_matches=skills_analysis.get("skill_matches", []),
                    overall_score=skills_analysis.get("overall_score", 0.0),
                    mandatory_skills_covered=skills_analysis.get("mandatory_skills_covered", 0),
                    total_mandatory_skills=skills_analysis.get("total_mandatory_skills", 0),
                    analysis_time=0.0,
                    strengths=[],
                    weaknesses=[],
                    recommendations=[]
                )
            else:
                logger.warning("No skills analysis in result")
                return ResumeSkillsAnalysisResponse(
                    success=False,
                    resume_id=resume_id,
                    vacancy_id=vacancy_id,
                    skill_matches=[],
                    overall_score=0.0,
                    mandatory_skills_covered=0,
                    total_mandatory_skills=0,
                    analysis_time=0.0,
                    strengths=[],
                    weaknesses=[],
                    recommendations=[],
                    error="No skills analysis available"
                )
                
        except Exception as e:
            logger.error(f"Exception in analyze_resume_with_dynamic_skills: {str(e)}")
            import traceback
            traceback.print_exc()
            return ResumeSkillsAnalysisResponse(
                success=False,
                resume_id=resume_id,
                vacancy_id=vacancy_id,
                skill_matches=[],
                overall_score=0.0,
                mandatory_skills_covered=0,
                total_mandatory_skills=0,
                analysis_time=0.0,
                strengths=[],
                weaknesses=[],
                recommendations=[],
                error=str(e)
            )
    
    async def create_vacancy_based_skills(self, resume_id: str) -> Dict[str, Any]:
        """
        Create skills based on vacancy requirements analysis
        
        Args:
            resume_id: ID of the resume
            
        Returns:
            Dict with result
        """
        try:
            resume = self.get_resume(resume_id)
            if not resume:
                return {"success": False, "error": "Resume not found"}
            
            if not resume.vacancy_id:
                return {"success": False, "error": "Resume not linked to vacancy"}
            
            # Get vacancy
            vacancy = self.db.query(Vacancy).filter(Vacancy.id == resume.vacancy_id).first()
            if not vacancy:
                return {"success": False, "error": "Vacancy not found"}
            
            # Extract skills from vacancy
            from app.services.vacancy_skills_extractor import VacancySkillsExtractor
            skills_extractor = VacancySkillsExtractor()
            vacancy_skills = await skills_extractor.extract_skills_from_vacancy(vacancy.id, force_reload=False)
            
            if not vacancy_skills:
                return {"success": False, "error": "No skills found in vacancy"}
            
            # Analyze resume against vacancy skills
            resume_text = self._extract_resume_text(resume.resume_blocks)
            
            from app.services.llm_resume_analyzer import LLMResumeAnalyzer
            llm_analyzer = LLMResumeAnalyzer()
            
            analysis_result = await llm_analyzer.analyze_resume_with_dynamic_skills(
                resume_text=resume_text,
                vacancy_skills=vacancy_skills,
                vacancy_id=vacancy.id
            )
            
            if not analysis_result.success:
                return {"success": False, "error": "Skills analysis failed"}
            
            # Clear existing skills
            existing_skills = self.db.query(ResumeSkill).filter(ResumeSkill.resume_id == resume.id).all()
            for existing_skill in existing_skills:
                self.db.delete(existing_skill)
            
            # Create new skills based on vacancy requirements
            skills_created = 0
            for skill_match in analysis_result.skill_matches:
                skill = ResumeSkill(
                    id=f"SKILL_{uuid.uuid4().hex[:8].upper()}",
                    resume_id=resume.id,
                    skill_name=skill_match.skill_name,
                    skill_category=skill_match.category or "general",
                    experience_level=skill_match.candidate_level or "intermediate",
                    confidence_score=skill_match.confidence or 50.0,
                    extracted_from=skill_match.context or ""
                )
                self.db.add(skill)
                skills_created += 1
            
            self.db.commit()
            
            return {
                "success": True,
                "skills_created": skills_created,
                "total_vacancy_skills": len(vacancy_skills),
                "analysis_result": analysis_result.dict()
            }
            
        except Exception as e:
            logger.error(f"Error creating vacancy-based skills: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def _create_resume_blocks(self, resume: Resume, sections: Dict[str, str]):
        """Create resume blocks from parsed sections"""
        logger.info(f"Creating resume blocks for resume {resume.id}")
        logger.info(f"Found sections: {list(sections.keys())}")
        
        for section_name, section_text in sections.items():
            logger.info(f"Processing section '{section_name}' with text length: {len(section_text)}")
            if section_text.strip():
                block = ResumeBlock(
                    id=f"BLOCK_{uuid.uuid4().hex[:8].upper()}",
                    resume_id=resume.id,
                    block_type=section_name,
                    block_name=section_name.replace('_', ' ').title(),
                    extracted_text=section_text,  # Полный текст без ограничений
                    relevance_score=50.0,  # Default score
                    confidence_score=80.0  # Default confidence
                )
                self.db.add(block)
                logger.info(f"Created block '{section_name}' with ID {block.id}")
            else:
                logger.warning(f"Section '{section_name}' has empty text, skipping")
        
        self.db.commit()
        logger.info(f"Successfully created {len([s for s in sections.values() if s.strip()])} blocks")
    
    async def analyze_skills_vs_vacancy_requirements(self, resume_id: str) -> Dict[str, Any]:
        """Analyze resume skills against vacancy requirements"""
        try:
            resume = self.get_resume(resume_id)
            if not resume or not resume.vacancy_id:
                return {"success": False, "error": "Resume not found or not linked to vacancy"}
            
            # Get vacancy
            vacancy = self.db.query(Vacancy).filter(Vacancy.id == resume.vacancy_id).first()
            if not vacancy:
                return {"success": False, "error": "Vacancy not found"}
            
            # Get vacancy keywords
            vacancy_keywords = self.db.query(VacancySectionKeywords).filter(
                VacancySectionKeywords.vacancy_id == vacancy.id
            ).all()
            
            if not vacancy_keywords:
                return {"success": False, "error": "No vacancy keywords found"}
            
            # Get resume skills
            resume_skills = self.db.query(ResumeSkill).filter(ResumeSkill.resume_id == resume.id).all()
            
            # Analyze skills against requirements
            from app.services.llm_resume_analyzer import LLMResumeAnalyzer
            llm_analyzer = LLMResumeAnalyzer()
            
            # Prepare vacancy requirements
            requirements_text = ""
            for kw in vacancy_keywords:
                if kw.keywords:
                    requirements_text += f"{kw.section_type}: {', '.join(kw.keywords)}\n"
            
            # Prepare resume skills
            skills_text = ""
            for skill in resume_skills:
                skills_text += f"- {skill.skill_name} ({skill.skill_category}): {skill.experience_level} level\n"
            
            # Create analysis prompt
            prompt = f"""
Ты - эксперт по оценке соответствия навыков кандидата требованиям вакансии.

ТРЕБОВАНИЯ ВАКАНСИИ:
{requirements_text}

НАВЫКИ КАНДИДАТА:
{skills_text}

ЗАДАЧА:
Оцени соответствие каждого навыка кандидата требованиям вакансии. Определи:
1. Насколько навык релевантен для вакансии (0-100%)
2. Есть ли прямое соответствие с требованиями
3. Общую оценку соответствия

ТРЕБУЕМЫЙ ФОРМАТ ОТВЕТА (JSON):
{{
    "skills_analysis": [
        {{
            "skill_name": "название навыка",
            "relevance_score": 85,
            "matches_requirements": true,
            "matched_keywords": ["ключевое слово 1", "ключевое слово 2"],
            "analysis": "подробный анализ соответствия"
        }}
    ],
    "overall_match_score": 75,
    "summary": "общая оценка соответствия навыков требованиям"
}}

ВАЖНО: Отвечай ТОЛЬКО в формате JSON.
"""
            
            # Call LLM
            llm_result = await llm_analyzer._call_llm_service(prompt)
            
            # Parse result
            import json
            try:
                json_start = llm_result.find('{')
                json_end = llm_result.rfind('}') + 1
                json_str = llm_result[json_start:json_end]
                result = json.loads(json_str)
                
                return {
                    "success": True,
                    "skills_analysis": result.get("skills_analysis", []),
                    "overall_match_score": result.get("overall_match_score", 0),
                    "summary": result.get("summary", "")
                }
                
            except Exception as e:
                logger.error(f"Failed to parse skills analysis: {str(e)}")
                return {"success": False, "error": f"Failed to parse analysis: {str(e)}"}
                
        except Exception as e:
            logger.error(f"Error in skills analysis: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def _extract_resume_text(self, resume_blocks: List[ResumeBlock]) -> str:
        """Extract text from resume blocks"""
        text_parts = []
        for block in resume_blocks:
            if block.extracted_text:
                text_parts.append(f"{block.block_type}: {block.extracted_text}")
        return "\n\n".join(text_parts)
    
    def _create_resume_skills(self, resume: Resume, skills: List[Dict[str, Any]]):
        """Create resume skills from parsed skills"""
        for skill_data in skills:
            skill = ResumeSkill(
                id=f"SKILL_{uuid.uuid4().hex[:8].upper()}",
                resume_id=resume.id,
                skill_name=skill_data["name"],
                skill_category=skill_data["category"],
                experience_level=skill_data.get("experience_level", "intermediate"),
                confidence_score=skill_data.get("confidence", 0.8) * 100,  # Convert to percentage
                extracted_from=skill_data.get("context", "")  # Полный контекст без ограничений
            )
            self.db.add(skill)
