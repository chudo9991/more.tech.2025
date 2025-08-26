"""
Scoring service for LLM-based answer evaluation
"""
import json
import asyncio
from typing import Dict, Any, List
import openai
from anthropic import Anthropic
import jsonschema

from app.core.config import settings


class ScoringService:
    def __init__(self):
        self.openai_client = None
        self.anthropic_client = None
        self._init_clients()

    def _init_clients(self):
        """Initialize LLM clients"""
        if settings.OPENAI_API_KEY:
            self.openai_client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        
        if settings.ANTHROPIC_API_KEY:
            self.anthropic_client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)

    async def score_answer(
        self,
        vacancy_id: str,
        question_id: str,
        question: str,
        answer_text: str,
        criteria: List[Dict[str, Any]],
        rubric_version: str = "v1"
    ) -> Dict[str, Any]:
        """Score an answer based on criteria"""
        try:
            # Prepare prompt
            prompt = self._create_scoring_prompt(
                question, answer_text, criteria, rubric_version
            )
            
            # Get LLM response
            response = await self._call_llm(prompt)
            
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

    def _create_scoring_prompt(
        self,
        question: str,
        answer_text: str,
        criteria: List[Dict[str, Any]],
        rubric_version: str
    ) -> str:
        """Create prompt for LLM scoring"""
        
        criteria_text = "\n".join([
            f"- {c['id']}: weight={c['weight']}, must_have={c.get('must_have', False)}, min_score={c.get('min_score', 0.0)}"
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

    async def _call_llm(self, prompt: str) -> str:
        """Call LLM API"""
        if self.openai_client:
            try:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a professional HR evaluator. Respond only with valid JSON."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=settings.LLM_TEMPERATURE,
                    max_tokens=settings.LLM_MAX_TOKENS
                )
                return response.choices[0].message.content
            except Exception as e:
                print(f"OpenAI call failed: {e}")
        
        if self.anthropic_client:
            try:
                response = self.anthropic_client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=settings.LLM_MAX_TOKENS,
                    temperature=settings.LLM_TEMPERATURE,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                return response.content[0].text
            except Exception as e:
                print(f"Anthropic call failed: {e}")
        
        # Fallback: return mock response
        return self._get_mock_response()

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
            repaired_response = await self._call_llm(repair_prompt)
            parsed_response = self._parse_llm_response(repaired_response)
            self._validate_response(parsed_response)
            return parsed_response
        except Exception as e:
            # Return fallback response
            return self._get_mock_response()

    def _get_mock_response(self) -> str:
        """Get mock response for testing"""
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
