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
                r'(?i)(компания|company|организация|organization)',
                r'(?i)(проекты на фриланс|freelance projects)',
                r'(?i)(август|январь|февраль|март|апрель|май|июнь|июль|сентябрь|октябрь|ноябрь|декабрь)\s+\d{4}'
            ],
            'education': [
                r'(?i)(образование|education|учебное заведение|university|college)',
                r'(?i)(диплом|degree|специальность|specialty)',
                r'(?i)(курсы|courses|обучение|training)',
                r'(?i)(институт|университет|академия|техникум)'
            ],
            'skills': [
                r'(?i)(навыки|skills|технологии|technologies|технические навыки)',
                r'(?i)(языки программирования|programming languages)',
                r'(?i)(инструменты|tools|фреймворки|frameworks)',
                r'(?i)(windows|linux|mac|python|java|sql|git|docker)'
            ],
            'projects': [
                r'(?i)(проекты|projects|портфолио|portfolio)',
                r'(?i)(разработка|development|создание|creation)',
                r'(?i)(реализованные проекты|completed projects)'
            ],
            'languages': [
                r'(?i)(языки|languages|иностранные языки|foreign languages)',
                r'(?i)(английский|english|русский|russian)',
                r'(?i)(уровень владения|proficiency level)'
            ],
            'certificates': [
                r'(?i)(сертификаты|certificates|сертификация|certification)',
                r'(?i)(аттестация|attestation|лицензии|licenses)',
                r'(?i)(полученные сертификаты|obtained certificates)'
            ],
            'personal_info': [
                r'(?i)(личная информация|personal information|контакты|contacts)',
                r'(?i)(имя|name|телефон|phone|email|почта)',
                r'(?i)(адрес|address|город|city)',
                r'(?i)(дата рождения|birth date|возраст|age)'
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
    
    async def parse_resume(self, text: str, vacancy_requirements: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Parse resume text and extract structured information
        
        Args:
            text: Raw resume text
            vacancy_requirements: Vacancy requirements for context-aware parsing
            
        Returns:
            Dict with structured resume data
        """
        try:
            # Clean and normalize text
            cleaned_text = self._clean_text(text)
            
            # Use LLM for intelligent parsing if vacancy requirements are provided
            if vacancy_requirements:
                try:
                    sections = await self._extract_sections_with_llm(cleaned_text, vacancy_requirements)
                except Exception as e:
                    print(f"DEBUG: LLM parsing failed, using regex fallback: {str(e)}")
                    sections = self._extract_sections(cleaned_text)
            else:
                sections = self._extract_sections(cleaned_text)
            
            # Debug logging
            print(f"DEBUG: Found {len(sections)} sections: {list(sections.keys())}")
            for section_name, section_text in sections.items():
                print(f"DEBUG: Section '{section_name}' has {len(section_text)} characters")
            
            # Extract skills
            skills = await self._extract_skills(cleaned_text)
            
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
    
    async def _extract_sections_with_llm(self, text: str, vacancy_requirements: Dict[str, Any]) -> Dict[str, str]:
        """Extract sections using LLM based on vacancy requirements"""
        try:
            # Import LLM service
            from app.services.llm_resume_analyzer import LLMResumeAnalyzer
            
            llm_analyzer = LLMResumeAnalyzer()
            
            # Create prompt for section extraction
            prompt = self._create_section_extraction_prompt(text, vacancy_requirements)
            
            # Call LLM
            llm_result = await llm_analyzer._call_llm_service(prompt)
            
            # Parse LLM response
            sections = self._parse_llm_sections_response(llm_result)
            
            return sections
            
        except Exception as e:
            print(f"DEBUG: LLM section extraction failed: {str(e)}, falling back to regex")
            return self._extract_sections(text)
    
    def _create_section_extraction_prompt(self, text: str, vacancy_requirements: Dict[str, Any]) -> str:
        """Create prompt for LLM-based section extraction"""
        prompt = f"""
Ты - эксперт по анализу резюме. Проанализируй текст резюме и раздели его на секции, соответствующие требованиям вакансии.

ТЕКСТ РЕЗЮМЕ:
{text}

ТРЕБОВАНИЯ ВАКАНСИИ:
- Обязанности: {vacancy_requirements.get('responsibilities', 'Не указано')}
- Требования: {vacancy_requirements.get('requirements', 'Не указано')}
- Специальные программы: {vacancy_requirements.get('programs', 'Не указано')}
- Дополнительная информация: {vacancy_requirements.get('additional', 'Не указано')}

ЗАДАЧА:
Раздели текст резюме на следующие секции, соответствующие структуре вакансии:

1. **experience** - Опыт работы, соответствующий обязанностям вакансии
2. **skills** - Навыки и технологии, соответствующие требованиям вакансии
3. **programs** - Опыт работы со специальными программами
4. **education** - Образование и обучение
5. **personal_info** - Личная информация и контакты

ТРЕБУЕМЫЙ ФОРМАТ ОТВЕТА (JSON):
{{
    "experience": "текст с опытом работы, соответствующим обязанностям вакансии",
    "skills": "текст с навыками, соответствующими требованиям вакансии", 
    "programs": "текст с опытом работы со специальными программами",
    "education": "текст с образованием и обучением",
    "personal_info": "текст с личной информацией"
}}

ВАЖНО:
- Каждая секция должна содержать релевантную информацию из резюме
- Если информация не найдена, оставь секцию пустой
- Сопоставляй опыт кандидата с требованиями вакансии
- Отвечай ТОЛЬКО в формате JSON, без дополнительного текста
"""
        return prompt
    
    def _parse_llm_sections_response(self, llm_response: str) -> Dict[str, str]:
        """Parse LLM response for sections"""
        try:
            import json
            
            # Extract JSON from response
            json_start = llm_response.find('{')
            json_end = llm_response.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON found in response")
            
            json_str = llm_response[json_start:json_end]
            sections = json.loads(json_str)
            
            # Ensure all required sections exist
            required_sections = ['experience', 'skills', 'programs', 'education', 'personal_info']
            for section in required_sections:
                if section not in sections:
                    sections[section] = ""
            
            return sections
            
        except Exception as e:
            print(f"DEBUG: Failed to parse LLM sections response: {str(e)}")
            return {}
    
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
        
        # Fallback: if no specific sections found, create sections based on content analysis
        if len(sections) <= 1:
            print(f"DEBUG: Using fallback section creation. Original sections: {list(sections.keys())}")
            sections = self._create_fallback_sections(text)
            print(f"DEBUG: After fallback, sections: {list(sections.keys())}")
        
        return sections
    
    def _create_fallback_sections(self, text: str) -> Dict[str, str]:
        """Create sections based on content analysis when explicit headers are not found"""
        sections = {}
        
        # Split text into lines and group by content type
        lines = text.split('\n')
        
        # Analyze content and assign to sections
        experience_content = []
        skills_content = []
        education_content = []
        personal_content = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            line_lower = line.lower()
            
            # Check for experience indicators
            if any(keyword in line_lower for keyword in ['опыт работы', 'место работы', 'компания', 'должность', 'проект', 'август', 'январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь', 'настоящее время', 'фриланс']):
                experience_content.append(line)
            # Check for skills indicators
            elif any(keyword in line_lower for keyword in ['навыки', 'технологии', 'windows', 'linux', 'mac', 'python', 'java', 'sql', 'git', 'docker', 'инструменты', 'dhcp', 'dns', 'gpo', 'service desk', '1c']):
                skills_content.append(line)
            # Check for education indicators
            elif any(keyword in line_lower for keyword in ['образование', 'университет', 'институт', 'диплом', 'курсы', 'обучение', 'специальность']):
                education_content.append(line)
            # Check for personal info indicators
            elif any(keyword in line_lower for keyword in ['имя', 'телефон', 'email', 'адрес', 'город', 'дата рождения', 'возраст']):
                personal_content.append(line)
            else:
                # Default to experience if no clear category
                experience_content.append(line)
        
        # Create sections
        if experience_content:
            sections['experience'] = '\n'.join(experience_content)
        if skills_content:
            sections['skills'] = '\n'.join(skills_content)
        if education_content:
            sections['education'] = '\n'.join(education_content)
        if personal_content:
            sections['personal_info'] = '\n'.join(personal_content)
        
        # If still no sections, force create multiple sections based on content
        if not sections:
            # Force split content into sections
            text_lower = text.lower()
            
            # Find experience section
            if any(keyword in text_lower for keyword in ['опыт работы', 'место работы', 'компания', 'должность']):
                sections['experience'] = text
            else:
                # Split text into chunks and assign to different sections
                lines = text.split('\n')
                chunk_size = len(lines) // 3
                
                if chunk_size > 0:
                    sections['experience'] = '\n'.join(lines[:chunk_size])
                    sections['skills'] = '\n'.join(lines[chunk_size:chunk_size*2])
                    sections['education'] = '\n'.join(lines[chunk_size*2:])
                else:
                    sections['experience'] = text
        
        print(f"DEBUG: Fallback created sections: {list(sections.keys())}")
        for section_name, section_text in sections.items():
            print(f"DEBUG: Fallback section '{section_name}' has {len(section_text)} characters")
        
        return sections
    
    async def _extract_skills(self, text: str) -> List[Dict[str, Any]]:
        """Extract skills from text using LLM analysis"""
        try:
            # Import LLM service
            from app.services.llm_resume_analyzer import LLMResumeAnalyzer
            
            llm_analyzer = LLMResumeAnalyzer()
            
            # Create prompt for skills extraction
            prompt = f"""
Ты - эксперт по анализу резюме. Проанализируй текст резюме и извлеки все технические навыки, технологии и инструменты, которыми владеет кандидат.

ТЕКСТ РЕЗЮМЕ:
{text}

ЗАДАЧА:
Извлеки все технические навыки, технологии, языки программирования, фреймворки, инструменты, которые упоминаются в резюме.

ТРЕБУЕМЫЙ ФОРМАТ ОТВЕТА (JSON):
{{
    "skills": [
        {{
            "name": "название навыка",
            "category": "категория (programming/frameworks/tools/databases/methodologies)",
            "confidence": 0.7,
            "context": "контекст из резюме, где упоминается навык",
            "experience_level": "beginner/intermediate/expert"
        }}
    ]
}}

ВАЖНО: 
- Извлекай только реальные навыки, которые явно упоминаются в резюме
- Не добавляй навыки, которых нет в тексте
- Оценивай уровень опыта на основе контекста
- Устанавливай confidence от 0.5 до 0.95 в зависимости от ясности упоминания навыка
- Отвечай ТОЛЬКО в формате JSON

ВАЖНО: 
- Извлекай только реальные навыки, которые явно упоминаются в резюме
- Не добавляй навыки, которых нет в тексте
- Оценивай уровень опыта на основе контекста
- Отвечай ТОЛЬКО в формате JSON
"""
            
            # Call LLM
            llm_result = await llm_analyzer._call_llm_service(prompt)
            
            # Parse LLM response
            import json
            try:
                # Extract JSON from response
                json_start = llm_result.find('{')
                json_end = llm_result.rfind('}') + 1
                
                if json_start == -1 or json_end == 0:
                    raise ValueError("No JSON found in response")
                
                json_str = llm_result[json_start:json_end]
                result = json.loads(json_str)
                
                return result.get("skills", [])
                
            except Exception as e:
                print(f"DEBUG: Failed to parse LLM skills response: {str(e)}")
                return []
                
        except Exception as e:
            print(f"DEBUG: LLM skills extraction failed: {str(e)}, falling back to regex")
            return self._extract_skills_fallback(text)
    
    def _extract_skills_fallback(self, text: str) -> List[Dict[str, Any]]:
        """Fallback regex-based skills extraction"""
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
                            "confidence": 0.6,  # Lower confidence for regex fallback
                            "context": self._extract_context(text, match.start(), match.end()),
                            "experience_level": "intermediate"  # Default level
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
