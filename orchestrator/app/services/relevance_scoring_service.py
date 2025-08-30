"""
Resume relevance scoring service
"""
from typing import Dict, List, Any, Optional
from decimal import Decimal
from app.models import Resume, ResumeBlock, ResumeSkill, Vacancy
from app.services.llm_resume_analyzer import llm_analyzer


class RelevanceScoringService:
    """Service for calculating resume relevance scores"""
    
    def __init__(self):
        # Scoring weights for different components
        self.weights = {
            "experience": 0.40,  # 40% - most important
            "skills": 0.30,      # 30% - technical skills
            "education": 0.20,   # 20% - education level
            "projects": 0.10     # 10% - project experience
        }
    
    async def calculate_resume_score(self, resume: Resume, vacancy: Vacancy) -> Dict[str, Any]:
        """
        Calculate overall relevance score for resume
        
        Args:
            resume: Resume object
            vacancy: Vacancy object
            
        Returns:
            Dict with scoring results
        """
        try:
            # Get resume blocks and skills
            resume_blocks = resume.resume_blocks
            resume_skills = resume.reskills
            
            # Extract vacancy requirements
            vacancy_requirements = self._extract_vacancy_requirements(vacancy)
            
            # Calculate component scores
            experience_score = await self._calculate_experience_score(resume_blocks, vacancy_requirements)
            skills_score = await self._calculate_skills_score(resume_skills, vacancy_requirements)
            education_score = await self._calculate_education_score(resume_blocks, vacancy_requirements)
            projects_score = await self._calculate_projects_score(resume_blocks, vacancy_requirements)
            
            # Calculate weighted total score
            total_score = (
                experience_score["score"] * self.weights["experience"] +
                skills_score["score"] * self.weights["skills"] +
                education_score["score"] * self.weights["education"] +
                projects_score["score"] * self.weights["projects"]
            )
            
            # Calculate confidence score
            confidence_score = self._calculate_confidence_score([
                experience_score["confidence"],
                skills_score["confidence"],
                education_score["confidence"],
                projects_score["confidence"]
            ])
            
            return {
                "success": True,
                "total_score": round(total_score, 2),
                "confidence_score": round(confidence_score, 2),
                "component_scores": {
                    "experience": experience_score,
                    "skills": skills_score,
                    "education": education_score,
                    "projects": projects_score
                },
                "weights": self.weights,
                "recommendation": self._get_recommendation(total_score),
                "strengths": self._identify_strengths(experience_score, skills_score, education_score, projects_score),
                "weaknesses": self._identify_weaknesses(experience_score, skills_score, education_score, projects_score)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "total_score": 0,
                "confidence_score": 0
            }
    
    def _extract_vacancy_requirements(self, vacancy: Vacancy) -> Dict[str, Any]:
        """Extract requirements from vacancy"""
        return {
            "title": vacancy.title,
            "required_skills": self._parse_skills_from_vacancy(vacancy),
            "experience_years": self._extract_experience_requirement(vacancy),
            "education_level": self._extract_education_requirement(vacancy),
            "description": vacancy.description or "",
            "requirements": vacancy.requirements or ""
        }
    
    def _parse_skills_from_vacancy(self, vacancy: Vacancy) -> List[str]:
        """Parse skills from vacancy description"""
        # This is a simplified implementation
        # In a real system, you might have structured skill requirements
        skills = []
        
        # Common tech skills to look for
        tech_skills = [
            "python", "java", "javascript", "typescript", "react", "vue", "angular",
            "django", "flask", "fastapi", "spring", "node.js", "express",
            "postgresql", "mysql", "mongodb", "redis", "elasticsearch",
            "docker", "kubernetes", "aws", "azure", "gcp", "git", "jenkins",
            "agile", "scrum", "devops", "ci/cd", "microservices", "api"
        ]
        
        description = (vacancy.description or "").lower()
        requirements = (vacancy.requirements or "").lower()
        
        for skill in tech_skills:
            if skill in description or skill in requirements:
                skills.append(skill)
        
        return skills
    
    def _extract_experience_requirement(self, vacancy: Vacancy) -> int:
        """Extract required experience years from vacancy"""
        # Simplified implementation
        # In a real system, this would be a structured field
        description = (vacancy.description or "").lower()
        
        # Look for experience patterns
        if "senior" in description or "lead" in description:
            return 5
        elif "middle" in description or "mid" in description:
            return 3
        elif "junior" in description or "entry" in description:
            return 1
        else:
            return 2  # Default
    
    def _extract_education_requirement(self, vacancy: Vacancy) -> str:
        """Extract education requirement from vacancy"""
        description = (vacancy.description or "").lower()
        
        if "phd" in description or "доктор" in description:
            return "phd"
        elif "master" in description or "магистр" in description:
            return "master"
        elif "bachelor" in description or "бакалавр" in description:
            return "bachelor"
        else:
            return "bachelor"  # Default
    
    async def _calculate_experience_score(self, resume_blocks: List[ResumeBlock], requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate experience relevance score"""
        try:
            # Find experience block
            experience_block = next((block for block in resume_blocks if block.block_type == "experience"), None)
            
            if not experience_block:
                return {"score": 0, "confidence": 0, "details": "No experience block found"}
            
            # Use LLM for detailed analysis
            llm_result = await llm_analyzer.analyze_experience_relevance(
                experience_block.extracted_text,
                requirements["description"]
            )
            
            if llm_result["success"]:
                analysis = llm_result["experience_analysis"]
                relevance_score = float(analysis.get("relevance_score", 0))
                confidence = 85  # High confidence for LLM analysis
            else:
                # Fallback to simple scoring
                relevance_score = self._simple_experience_scoring(experience_block.extracted_text, requirements)
                confidence = 60
            
            return {
                "score": relevance_score,
                "confidence": confidence,
                "details": llm_result.get("experience_analysis", {})
            }
            
        except Exception as e:
            return {"score": 0, "confidence": 0, "details": f"Error: {str(e)}"}
    
    async def _calculate_skills_score(self, resume_skills: List[ResumeSkill], requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate skills relevance score"""
        try:
            required_skills = requirements["required_skills"]
            
            if not required_skills:
                return {"score": 50, "confidence": 50, "details": "No required skills specified"}
            
            # Extract skill names
            candidate_skills = [skill.skill_name.lower() for skill in resume_skills]
            
            # Use LLM for detailed skills analysis
            llm_result = await llm_analyzer.analyze_skills_match(candidate_skills, required_skills)
            
            if llm_result["success"]:
                analysis = llm_result["skills_analysis"]
                match_percentage = float(analysis.get("match_percentage", 0))
                confidence = 80
                details = analysis
            else:
                # Fallback to simple matching
                matched_skills = [skill for skill in required_skills if skill.lower() in candidate_skills]
                match_percentage = (len(matched_skills) / len(required_skills)) * 100
                confidence = 70
                details = {
                    "matched_skills": matched_skills,
                    "missing_skills": [skill for skill in required_skills if skill.lower() not in candidate_skills]
                }
            
            return {
                "score": match_percentage,
                "confidence": confidence,
                "details": details
            }
            
        except Exception as e:
            return {"score": 0, "confidence": 0, "details": f"Error: {str(e)}"}
    
    async def _calculate_education_score(self, resume_blocks: List[ResumeBlock], requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate education relevance score"""
        try:
            education_block = next((block for block in resume_blocks if block.block_type == "education"), None)
            
            if not education_block:
                return {"score": 0, "confidence": 0, "details": "No education block found"}
            
            required_level = requirements["education_level"]
            
            # Simple education level scoring
            education_levels = {
                "phd": 100,
                "master": 80,
                "bachelor": 60,
                "high_school": 30
            }
            
            # Determine candidate's education level from text
            text = education_block.extracted_text.lower()
            candidate_level = "bachelor"  # Default
            
            if "phd" in text or "доктор" in text or "кандидат" in text:
                candidate_level = "phd"
            elif "master" in text or "магистр" in text:
                candidate_level = "master"
            elif "bachelor" in text or "бакалавр" in text:
                candidate_level = "bachelor"
            
            # Calculate score based on level comparison
            candidate_score = education_levels.get(candidate_level, 50)
            required_score = education_levels.get(required_level, 60)
            
            if candidate_score >= required_score:
                score = 100
            else:
                score = (candidate_score / required_score) * 100
            
            return {
                "score": score,
                "confidence": 75,
                "details": {
                    "candidate_level": candidate_level,
                    "required_level": required_level,
                    "score": score
                }
            }
            
        except Exception as e:
            return {"score": 0, "confidence": 0, "details": f"Error: {str(e)}"}
    
    async def _calculate_projects_score(self, resume_blocks: List[ResumeBlock], requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate projects relevance score"""
        try:
            projects_block = next((block for block in resume_blocks if block.block_type == "projects"), None)
            
            if not projects_block:
                return {"score": 0, "confidence": 0, "details": "No projects block found"}
            
            # Simple scoring based on project count and relevance
            text = projects_block.extracted_text.lower()
            required_skills = requirements["required_skills"]
            
            # Count projects (simple heuristic)
            project_indicators = ["проект", "project", "разработка", "development", "создание", "creation"]
            project_count = sum(1 for indicator in project_indicators if indicator in text)
            
            # Check for relevant skills in projects
            relevant_mentions = sum(1 for skill in required_skills if skill.lower() in text)
            
            # Calculate score
            if project_count == 0:
                score = 0
            elif project_count >= 3 and relevant_mentions >= len(required_skills) * 0.5:
                score = 100
            elif project_count >= 2 and relevant_mentions >= len(required_skills) * 0.3:
                score = 80
            elif project_count >= 1 and relevant_mentions >= len(required_skills) * 0.2:
                score = 60
            else:
                score = 30
            
            return {
                "score": score,
                "confidence": 65,
                "details": {
                    "project_count": project_count,
                    "relevant_mentions": relevant_mentions,
                    "required_skills_count": len(required_skills)
                }
            }
            
        except Exception as e:
            return {"score": 0, "confidence": 0, "details": f"Error: {str(e)}"}
    
    def _simple_experience_scoring(self, experience_text: str, requirements: Dict[str, Any]) -> float:
        """Simple experience scoring fallback"""
        required_years = requirements["experience_years"]
        text = experience_text.lower()
        
        # Look for year patterns
        import re
        year_patterns = [
            r'(\d{4})\s*-\s*(\d{4})',
            r'(\d{4})\s*-\s*(present|current|настоящее)',
            r'(\d+)\s*(лет|years|год|year)'
        ]
        
        total_years = 0
        for pattern in year_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                if len(match) == 2:
                    if match[1].lower() in ['present', 'current', 'настоящее']:
                        # Assume current year
                        total_years += 2024 - int(match[0])
                    else:
                        total_years += int(match[1]) - int(match[0])
                elif len(match) == 2 and match[1].isdigit():
                    total_years += int(match[1])
        
        if total_years >= required_years:
            return 100
        elif total_years >= required_years * 0.7:
            return 80
        elif total_years >= required_years * 0.5:
            return 60
        else:
            return max(20, (total_years / required_years) * 100)
    
    def _calculate_confidence_score(self, confidences: List[float]) -> float:
        """Calculate overall confidence score"""
        if not confidences:
            return 0
        
        # Weighted average based on component importance
        weights = [self.weights["experience"], self.weights["skills"], 
                  self.weights["education"], self.weights["projects"]]
        
        weighted_sum = sum(conf * weight for conf, weight in zip(confidences, weights))
        return weighted_sum
    
    def _get_recommendation(self, total_score: float) -> str:
        """Get hiring recommendation based on score"""
        if total_score >= 80:
            return "hire"
        elif total_score >= 60:
            return "consider"
        else:
            return "reject"
    
    def _identify_strengths(self, experience_score: Dict, skills_score: Dict, 
                           education_score: Dict, projects_score: Dict) -> List[str]:
        """Identify candidate strengths"""
        strengths = []
        
        if experience_score["score"] >= 80:
            strengths.append("Strong relevant experience")
        if skills_score["score"] >= 80:
            strengths.append("Excellent technical skills match")
        if education_score["score"] >= 80:
            strengths.append("High education level")
        if projects_score["score"] >= 80:
            strengths.append("Relevant project experience")
        
        return strengths
    
    def _identify_weaknesses(self, experience_score: Dict, skills_score: Dict,
                            education_score: Dict, projects_score: Dict) -> List[str]:
        """Identify candidate weaknesses"""
        weaknesses = []
        
        if experience_score["score"] < 50:
            weaknesses.append("Insufficient relevant experience")
        if skills_score["score"] < 50:
            weaknesses.append("Missing key technical skills")
        if education_score["score"] < 50:
            weaknesses.append("Education level below requirements")
        if projects_score["score"] < 50:
            weaknesses.append("Limited relevant project experience")
        
        return weaknesses


# Global instance
relevance_scorer = RelevanceScoringService()
