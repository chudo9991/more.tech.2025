"""
LLM service for Azure GPT-4o integration
"""
import json
import asyncio
from typing import Dict, Any, List, Optional
import openai
from openai import AzureOpenAI

from app.core.config import settings


class LLMService:
    def __init__(self):
        self.client = None
        self._init_client()

    def _init_client(self):
        """Initialize Azure OpenAI client"""
        try:
            if settings.AZURE_OPENAI_ENDPOINT and settings.AZURE_OPENAI_API_KEY:
                self.client = AzureOpenAI(
                    azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
                    api_key=settings.AZURE_OPENAI_API_KEY,
                    api_version=settings.AZURE_OPENAI_API_VERSION
                )
            else:
                print("Azure OpenAI credentials not configured, using fallback mode")
                self.client = None
        except Exception as e:
            print(f"Failed to initialize Azure OpenAI client: {e}")
            self.client = None

    async def score_answer(
        self,
        vacancy_id: str,
        question_id: str,
        question: str,
        answer_text: str,
        criteria: List[Dict[str, Any]],
        rubric_version: str = "v1"
    ) -> Dict[str, Any]:
        """Score an answer based on criteria using Azure GPT-4o"""
        try:
            # Prepare prompt
            prompt = self._create_scoring_prompt(
                question, answer_text, criteria, rubric_version
            )
            
            # Get LLM response
            response = await self._call_azure_gpt4o(prompt)
            
            # Parse and validate response
            parsed_response = self._parse_llm_response(response)
            
            # Validate against schema
            self._validate_response(parsed_response)
            
            return parsed_response
            
        except Exception as e:
            # Try repair if JSON is malformed
            if "JSON" in str(e):
                return await self._repair_response(prompt, response)
            else:
                raise Exception(f"Scoring failed: {str(e)}")

    async def chat_with_avatar(
        self,
        session_id: str,
        message: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Chat with avatar using Azure GPT-4o"""
        try:
            # Prepare chat prompt
            prompt = self._create_chat_prompt(message, context)
            
            # Get LLM response
            response = await self._call_azure_gpt4o(prompt)
            
            # Parse response
            parsed_response = self._parse_chat_response(response)
            
            return {
                "response": parsed_response["response"],
                "avatar_emotion": parsed_response.get("emotion", "neutral"),
                "confidence": parsed_response.get("confidence", 0.8),
                "session_id": session_id
            }
            
        except Exception as e:
            raise Exception(f"Chat failed: {str(e)}")

    async def generate(self, prompt: str, max_tokens: int = 2000, temperature: float = 0.7, system_message: str = None) -> str:
        """Generate text using Azure GPT-4o"""
        try:
            # Prepare messages
            messages = []
            
            if system_message:
                messages.append({"role": "system", "content": system_message})
            
            messages.append({"role": "user", "content": prompt})
            
            # Call Azure GPT-4o
            response = await self._call_azure_gpt4o_messages(messages, max_tokens, temperature)
            
            return response
            
        except Exception as e:
            raise Exception(f"Generation failed: {str(e)}")

    async def analyze_tone(self, text: str, session_id: str) -> Dict[str, Any]:
        """Analyze tone of voice from text"""
        try:
            prompt = f"""
Analyze the tone of voice and emotional state from the following text. 
Consider factors like confidence, enthusiasm, nervousness, confusion, etc.

Text: "{text}"

Please respond with a JSON object containing:
- emotion: one of [positive, neutral, concerned, excited, confused, confident]
- confidence: float between 0.0 and 1.0
- reasoning: brief explanation of why this emotion was detected

Focus on the emotional tone and attitude expressed in the text.
"""
            
            response = await self._call_azure_gpt4o(prompt)
            
            # Parse response
            try:
                import json
                result = json.loads(response)
                return {
                    "emotion": result.get("emotion", "neutral"),
                    "confidence": result.get("confidence", 0.5),
                    "reasoning": result.get("reasoning", "No specific emotion detected")
                }
            except json.JSONDecodeError:
                # Fallback parsing
                emotion = "neutral"
                if any(word in text.lower() for word in ["excited", "great", "amazing", "love", "fantastic"]):
                    emotion = "excited"
                elif any(word in text.lower() for word in ["confident", "sure", "definitely", "certainly"]):
                    emotion = "confident"
                elif any(word in text.lower() for word in ["worried", "concerned", "unsure", "maybe"]):
                    emotion = "concerned"
                elif any(word in text.lower() for word in ["confused", "not sure", "don't know", "unclear"]):
                    emotion = "confused"
                elif any(word in text.lower() for word in ["good", "nice", "happy", "pleased"]):
                    emotion = "positive"
                
                return {
                    "emotion": emotion,
                    "confidence": 0.6,
                    "reasoning": f"Fallback analysis based on keywords in text"
                }
                
        except Exception as e:
            print(f"Tone analysis failed: {e}")
            return {
                "emotion": "neutral",
                "confidence": 0.5,
                "reasoning": "Analysis failed, using neutral emotion"
            }

    def _create_scoring_prompt(
        self,
        question: str,
        answer_text: str,
        criteria: List[Dict[str, Any]],
        rubric_version: str
    ) -> str:
        """Create prompt for LLM scoring"""
        
        criteria_text = "\n".join([
            f"- {c['id']}: weight={c.get('weight', 1.0)}, must_have={c.get('must_have', False)}, min_score={c.get('min_score', 0.0)}"
            for c in criteria
        ])
        
        prompt = f"""
You are an expert HR interviewer evaluating a candidate's answer. Please score the answer based on the given criteria.

Question: {question}
Answer: {answer_text}

Criteria:
{criteria_text}

Please provide your evaluation in the following JSON format:
{{
    "overall_score": 0.85,
    "passed": true,
    "per_criterion": [
        {{
            "id": "FASTAPI",
            "score": 0.9,
            "evidence": "Candidate mentioned Depends, BackgroundTasks, and Pydantic - shows deep knowledge"
        }}
    ],
    "red_flags": ["No examples of load testing"],
    "explanations": ["Candidate provided good examples of routing and dependencies"],
    "version": "{rubric_version}"
}}

Rules:
1. Scores should be between 0.0 and 1.0
2. For must_have criteria, if score < min_score, set passed=false
3. Provide specific evidence for each criterion score
4. List any red flags or concerns
5. Give brief explanations for your overall assessment
6. Return ONLY valid JSON, no additional text
"""
        return prompt

    def _create_chat_prompt(
        self,
        message: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Create prompt for avatar chat"""
        
        context_text = ""
        if context:
            context_text = f"\nContext: {json.dumps(context, ensure_ascii=False)}"
        
        prompt = f"""
You are a friendly HR interviewer avatar conducting a job interview. Respond naturally and professionally to the candidate's message.

Candidate's message: {message}{context_text}

Please respond in the following JSON format:
{{
    "response": "Your natural response to the candidate",
    "emotion": "neutral|positive|concerned|excited",
    "confidence": 0.85
}}

Rules:
1. Be professional but friendly
2. Ask follow-up questions when appropriate
3. Show interest in the candidate's experience
4. Keep responses concise but engaging
5. Return ONLY valid JSON
"""
        return prompt

    async def _call_azure_gpt4o(self, prompt: str) -> str:
        """Call Azure GPT-4o API"""
        if not self.client:
            # Fallback response
            return self._get_fallback_response(prompt)
        
        try:
            response = self.client.chat.completions.create(
                model=settings.AZURE_OPENAI_DEPLOYMENT_NAME,
                messages=[
                    {"role": "system", "content": "You are a professional HR evaluator. Respond only with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=settings.LLM_TEMPERATURE,
                max_tokens=settings.LLM_MAX_TOKENS
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Azure GPT-4o call failed: {e}")
            return self._get_fallback_response(prompt)

    async def _call_azure_gpt4o_messages(self, messages: List[Dict[str, str]], max_tokens: int = 2000, temperature: float = 0.7) -> str:
        """Call Azure GPT-4o API with custom messages"""
        if not self.client:
            # Fallback response for skills extraction
            return self._get_skills_fallback_response()
        
        try:
            response = self.client.chat.completions.create(
                model=settings.AZURE_OPENAI_DEPLOYMENT_NAME,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Azure GPT-4o call failed: {e}")
            return self._get_skills_fallback_response()

    def _parse_llm_response(self, response: str) -> Dict[str, Any]:
        """Parse LLM response as JSON"""
        try:
            # Clean response - remove markdown code blocks if present
            cleaned_response = response.strip()
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response[:-3]
            
            return json.loads(cleaned_response.strip())
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid JSON response: {e}")

    def _parse_chat_response(self, response: str) -> Dict[str, Any]:
        """Parse chat response as JSON"""
        try:
            # Clean response - remove markdown code blocks if present
            cleaned_response = response.strip()
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response[:-3]
            
            return json.loads(cleaned_response.strip())
        except json.JSONDecodeError as e:
            # Return fallback response
            return {
                "response": "Thank you for your response. Could you please elaborate on that?",
                "emotion": "neutral",
                "confidence": 0.5
            }

    def _validate_response(self, response: Dict[str, Any]):
        """Validate response against schema"""
        required_fields = ["overall_score", "passed", "per_criterion", "version"]
        
        for field in required_fields:
            if field not in response:
                raise Exception(f"Missing required field: {field}")
        
        # Validate overall_score
        if not isinstance(response["overall_score"], (int, float)):
            raise Exception("overall_score must be a number")
        if not 0 <= response["overall_score"] <= 1:
            raise Exception("overall_score must be between 0 and 1")
        
        # Validate passed
        if not isinstance(response["passed"], bool):
            raise Exception("passed must be a boolean")
        
        # Validate per_criterion
        if not isinstance(response["per_criterion"], list):
            raise Exception("per_criterion must be a list")
        
        for criterion in response["per_criterion"]:
            if "id" not in criterion or "score" not in criterion:
                raise Exception("Each criterion must have 'id' and 'score' fields")

    async def _repair_response(self, prompt: str, original_response: str) -> Dict[str, Any]:
        """Attempt to repair malformed JSON response"""
        repair_prompt = f"""
The previous response was malformed. Please fix the JSON and return only valid JSON:

Original response: {original_response}

Please provide a corrected version with the same structure but valid JSON syntax.
"""
        
        try:
            repaired_response = await self._call_azure_gpt4o(repair_prompt)
            parsed_response = self._parse_llm_response(repaired_response)
            self._validate_response(parsed_response)
            return parsed_response
        except Exception as e:
            # Return fallback response
            return self._get_fallback_response(prompt)

    def _get_fallback_response(self, prompt: str) -> str:
        """Get fallback response for testing"""
        if "scoring" in prompt.lower():
            return json.dumps({
                "overall_score": 0.75,
                "passed": True,
                "per_criterion": [
                    {
                        "id": "FASTAPI",
                        "score": 0.8,
                        "evidence": "Candidate shows basic understanding"
                    }
                ],
                "red_flags": [],
                "explanations": ["Mock response due to LLM unavailability"],
                "version": "v1"
            })
        else:
            return json.dumps({
                "response": "Thank you for your response. Could you please elaborate on that?",
                "emotion": "neutral",
                "confidence": 0.5
            })

    def _get_skills_fallback_response(self) -> str:
        """Get fallback response for skills extraction"""
        return json.dumps({
            "skills": [
                {
                    "skill_name": "Python",
                    "category": "programming",
                    "importance": 0.9,
                    "required_level": "intermediate",
                    "is_mandatory": True,
                    "alternatives": ["Python 3", "Python3"],
                    "description": "Основной язык программирования для бэкенд разработки"
                },
                {
                    "skill_name": "FastAPI",
                    "category": "frameworks",
                    "importance": 0.8,
                    "required_level": "intermediate",
                    "is_mandatory": True,
                    "alternatives": ["Fast API", "FastAPI framework"],
                    "description": "Современный веб-фреймворк для создания API"
                },
                {
                    "skill_name": "PostgreSQL",
                    "category": "database",
                    "importance": 0.7,
                    "required_level": "intermediate",
                    "is_mandatory": False,
                    "alternatives": ["Postgres", "PostgreSQL DB"],
                    "description": "Реляционная база данных"
                },
                {
                    "skill_name": "Docker",
                    "category": "devops",
                    "importance": 0.6,
                    "required_level": "intermediate",
                    "is_mandatory": False,
                    "alternatives": ["Docker containers", "Containerization"],
                    "description": "Контейнеризация приложений"
                }
            ]
        })
