"""
Resume parsing and structuring service
"""
import re
from typing import Dict, List, Any, Optional
from datetime import datetime


class ResumeParserService:
    """Service for parsing and structuring resume text"""
    
    def __init__(self):
        # Common section headers in different languages
        self.section_patterns = {
            'experience': [
                r'(?i)(опыт работы|work experience|experience|employment history|трудовая деятельность)',
                r'(?i)(место работы|job|position|должность)',
                r'(?i)(компания|company|организация|organization)'
            ],
            'education': [
                r'(?i)(образование|education|учебное заведение|university|college)',
                r'(?i)(диплом|degree|специальность|specialty)',
                r'(?i)(курсы|courses|обучение|training)'
            ],
            'skills': [
                r'(?i)(навыки|skills|технологии|technologies|технические навыки)',
                r'(?i)(языки программирования|programming languages)',
                r'(?i)(инструменты|tools|фреймворки|frameworks)'
            ],
            'projects': [
                r'(?i)(проекты|projects|портфолио|portfolio)',
                r'(?i)(разработка|development|создание|creation)'
            ],
            'languages': [
                r'(?i)(языки|languages|иностранные языки|foreign languages)',
                r'(?i)(английский|english|русский|russian)'
            ],
            'certificates': [
                r'(?i)(сертификаты|certificates|сертификация|certification)',
                r'(?i)(аттестация|attestation|лицензии|licenses)'
            ],
            'personal_info': [
                r'(?i)(личная информация|personal information|контакты|contacts)',
                r'(?i)(имя|name|телефон|phone|email|почта)',
                r'(?i)(адрес|address|город|city)'
            ]
        }
        
        # Skill patterns for different categories
        self.skill_patterns = {
            'programming': [
                r'(?i)(python|java|c\+\+|c#|javascript|typescript|php|ruby|go|rust|swift|kotlin)',
                r'(?i)(html|css|sql|nosql|mongodb|postgresql|mysql|redis)'
            ],
            'frameworks': [
                r'(?i)(django|flask|fastapi|spring|express|react|vue|angular|node\.js)',
                r'(?i)(bootstrap|tailwind|jquery|axios|lodash)'
            ],
            'tools': [
                r'(?i)(git|docker|kubernetes|jenkins|gitlab|github|bitbucket)',
                r'(?i)(aws|azure|gcp|heroku|digitalocean|nginx|apache)'
            ],
            'databases': [
                r'(?i)(postgresql|mysql|mongodb|redis|elasticsearch|cassandra)',
                r'(?i)(oracle|sql server|sqlite|dynamodb)'
            ],
            'methodologies': [
                r'(?i)(agile|scrum|kanban|waterfall|devops|ci/cd)',
                r'(?i)(tdd|bdd|pair programming|code review)'
            ]
        }
    
    def parse_resume(self, text: str) -> Dict[str, Any]:
        """
        Parse resume text and extract structured information
        
        Args:
            text: Raw resume text
            
        Returns:
            Dict with structured resume data
        """
        try:
            # Clean and normalize text
            cleaned_text = self._clean_text(text)
            
            # Extract sections
            sections = self._extract_sections(cleaned_text)
            
            # Extract skills
            skills = self._extract_skills(cleaned_text)
            
            # Extract experience
            experience = self._extract_experience(sections.get('experience', ''))
            
            # Extract education
            education = self._extract_education(sections.get('education', ''))
            
            # Extract personal info
            personal_info = self._extract_personal_info(sections.get('personal_info', ''))
            
            return {
                "success": True,
                "sections": sections,
                "skills": skills,
                "experience": experience,
                "education": education,
                "personal_info": personal_info,
                "summary": {
                    "total_sections": len(sections),
                    "total_skills": len(skills),
                    "experience_years": self._calculate_experience_years(experience),
                    "education_level": self._determine_education_level(education)
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "sections": {},
                "skills": [],
                "experience": [],
                "education": [],
                "personal_info": {},
                "summary": {}
            }
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep important ones
        text = re.sub(r'[^\w\s\-\.\,\;\:\!\?\(\)\[\]\{\}\@\#\$\%\&\*\+\=\/\|\\]', '', text)
        
        # Normalize line breaks
        text = re.sub(r'\r\n', '\n', text)
        text = re.sub(r'\r', '\n', text)
        
        return text.strip()
    
    def _extract_sections(self, text: str) -> Dict[str, str]:
        """Extract different sections from resume text"""
        sections = {}
        lines = text.split('\n')
        
        current_section = 'general'
        current_content = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if line is a section header
            section_found = False
            for section_name, patterns in self.section_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, line):
                        # Save previous section
                        if current_content:
                            sections[current_section] = '\n'.join(current_content)
                        
                        # Start new section
                        current_section = section_name
                        current_content = [line]
                        section_found = True
                        break
                if section_found:
                    break
            
            if not section_found:
                current_content.append(line)
        
        # Save last section
        if current_content:
            sections[current_section] = '\n'.join(current_content)
        
        return sections
    
    def _extract_skills(self, text: str) -> List[Dict[str, Any]]:
        """Extract skills from text"""
        skills = []
        
        for category, patterns in self.skill_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    skill_name = match.group(0).lower()
                    
                    # Check if skill already exists
                    existing_skill = next((s for s in skills if s['name'].lower() == skill_name), None)
                    if not existing_skill:
                        skills.append({
                            "name": skill_name,
                            "category": category,
                            "confidence": 0.8,
                            "context": self._extract_context(text, match.start(), match.end())
                        })
        
        return skills
    
    def _extract_experience(self, experience_text: str) -> List[Dict[str, Any]]:
        """Extract work experience information"""
        experience = []
        
        if not experience_text:
            return experience
        
        # Simple pattern matching for experience
        # This is a basic implementation - can be enhanced with more sophisticated parsing
        
        # Look for date patterns
        date_patterns = [
            r'(\d{4})\s*-\s*(\d{4}|\bpresent\b|\bcurrent\b)',
            r'(\d{2}\.\d{2}\.\d{4})\s*-\s*(\d{2}\.\d{2}\.\d{4}|\bpresent\b|\bcurrent\b)',
            r'(\w+\s+\d{4})\s*-\s*(\w+\s+\d{4}|\bpresent\b|\bcurrent\b)'
        ]
        
        lines = experience_text.split('\n')
        current_experience = {}
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check for date patterns
            for pattern in date_patterns:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    if current_experience:
                        experience.append(current_experience)
                    
                    current_experience = {
                        "start_date": match.group(1),
                        "end_date": match.group(2) if match.group(2).lower() not in ['present', 'current'] else 'present',
                        "description": line
                    }
                    break
            
            if current_experience and 'description' in current_experience:
                current_experience['description'] += ' ' + line
        
        # Add last experience
        if current_experience:
            experience.append(current_experience)
        
        return experience
    
    def _extract_education(self, education_text: str) -> List[Dict[str, Any]]:
        """Extract education information"""
        education = []
        
        if not education_text:
            return education
        
        # Basic education extraction
        lines = education_text.split('\n')
        current_education = {}
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Look for degree patterns
            degree_patterns = [
                r'(?i)(бакалавр|bachelor|магистр|master|доктор|phd|кандидат|candidate)',
                r'(?i)(специалист|specialist|инженер|engineer)'
            ]
            
            for pattern in degree_patterns:
                match = re.search(pattern, line)
                if match:
                    if current_education:
                        education.append(current_education)
                    
                    current_education = {
                        "degree": match.group(0),
                        "description": line
                    }
                    break
            
            if current_education and 'description' in current_education:
                current_education['description'] += ' ' + line
        
        # Add last education
        if current_education:
            education.append(current_education)
        
        return education
    
    def _extract_personal_info(self, personal_text: str) -> Dict[str, Any]:
        """Extract personal information"""
        personal_info = {}
        
        if not personal_text:
            return personal_info
        
        # Extract email
        email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', personal_text)
        if email_match:
            personal_info['email'] = email_match.group(0)
        
        # Extract phone
        phone_match = re.search(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{2}[-.\s]?\d{2}', personal_text)
        if phone_match:
            personal_info['phone'] = phone_match.group(0)
        
        # Extract name (basic pattern)
        name_match = re.search(r'([А-ЯЁ][а-яё]+\s+[А-ЯЁ][а-яё]+|[A-Z][a-z]+\s+[A-Z][a-z]+)', personal_text)
        if name_match:
            personal_info['name'] = name_match.group(0)
        
        return personal_info
    
    def _extract_context(self, text: str, start: int, end: int) -> str:
        """Extract context around a match"""
        context_start = max(0, start - 50)
        context_end = min(len(text), end + 50)
        return text[context_start:context_end].strip()
    
    def _calculate_experience_years(self, experience: List[Dict[str, Any]]) -> float:
        """Calculate total years of experience"""
        total_years = 0.0
        
        for exp in experience:
            try:
                start_date = exp.get('start_date', '')
                end_date = exp.get('end_date', '')
                
                if start_date and end_date:
                    # Simple year extraction
                    start_year = re.search(r'\d{4}', start_date)
                    end_year = re.search(r'\d{4}', end_date) if end_date != 'present' else None
                    
                    if start_year:
                        start_year = int(start_year.group(0))
                        if end_year:
                            end_year = int(end_year.group(0))
                            total_years += (end_year - start_year)
                        else:
                            # If end date is present, calculate from start to current year
                            current_year = datetime.now().year
                            total_years += (current_year - start_year)
            except:
                continue
        
        return round(total_years, 1)
    
    def _determine_education_level(self, education: List[Dict[str, Any]]) -> str:
        """Determine highest education level"""
        levels = {
            'phd': 5,
            'candidate': 4,
            'master': 3,
            'bachelor': 2,
            'specialist': 2,
            'engineer': 2,
            'high_school': 1
        }
        
        highest_level = 'high_school'
        highest_score = 1
        
        for edu in education:
            degree = edu.get('degree', '').lower()
            for level, score in levels.items():
                if level in degree and score > highest_score:
                    highest_level = level
                    highest_score = score
        
        return highest_level


# Global instance
resume_parser = ResumeParserService()
