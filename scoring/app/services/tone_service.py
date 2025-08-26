"""
Tone analysis service for scoring
"""
import re
from typing import Dict, Any
import numpy as np
from textblob import TextBlob


class ToneService:
    def __init__(self):
        self.positive_words = {
            'ru': ['отлично', 'хорошо', 'успешно', 'эффективно', 'решил', 'оптимизировал', 'улучшил'],
            'en': ['excellent', 'good', 'successful', 'effective', 'solved', 'optimized', 'improved']
        }
        self.negative_words = {
            'ru': ['проблема', 'ошибка', 'неудача', 'сложно', 'трудно', 'не смог'],
            'en': ['problem', 'error', 'failure', 'difficult', 'hard', 'could not']
        }

    async def analyze_tone(
        self,
        text: str,
        language: str = "ru"
    ) -> Dict[str, Any]:
        """Analyze tone and paralinguistic features of text"""
        try:
            # Analyze tone
            tone_result = self._analyze_text_tone(text, language)
            
            # Calculate paralinguistic features
            paraling = self._calculate_paralinguistic(text)
            
            return {
                "tone": tone_result["tone"],
                "confidence": tone_result["confidence"],
                "paraling": paraling
            }
            
        except Exception as e:
            # Return neutral tone as fallback
            return {
                "tone": "neutral",
                "confidence": 0.5,
                "paraling": {
                    "answer_duration_s": 0.0,
                    "pre_answer_pause_s": 0.0,
                    "avg_silence_ratio": 0.0,
                    "speech_rate_wpm": 0.0
                }
            }

    def _analyze_text_tone(self, text: str, language: str) -> Dict[str, Any]:
        """Analyze the tone of text"""
        try:
            # Simple rule-based analysis
            text_lower = text.lower()
            
            # Count positive and negative words
            pos_count = sum(1 for word in self.positive_words.get(language, []) 
                          if word in text_lower)
            neg_count = sum(1 for word in self.negative_words.get(language, []) 
                          if word in text_lower)
            
            # Calculate tone score
            total_words = len(text.split())
            if total_words == 0:
                return {"tone": "neutral", "confidence": 0.5}
            
            pos_ratio = pos_count / total_words
            neg_ratio = neg_count / total_words
            
            # Determine tone
            if pos_ratio > neg_ratio and pos_ratio > 0.01:
                tone = "positive"
                confidence = min(pos_ratio * 10, 0.95)
            elif neg_ratio > pos_ratio and neg_ratio > 0.01:
                tone = "negative"
                confidence = min(neg_ratio * 10, 0.95)
            else:
                tone = "neutral"
                confidence = 0.7
            
            return {
                "tone": tone,
                "confidence": confidence
            }
            
        except Exception as e:
            print(f"Tone analysis failed: {e}")
            return {"tone": "neutral", "confidence": 0.5}

    def _calculate_paralinguistic(self, text: str) -> Dict[str, float]:
        """Calculate paralinguistic features from text"""
        try:
            # Estimate speech duration (assuming average speaking rate)
            words = text.split()
            word_count = len(words)
            
            # Average speaking rate: 130 words per minute
            avg_wpm = 130
            estimated_duration_s = word_count / avg_wpm * 60
            
            # Estimate pre-answer pause (based on text structure)
            sentences = text.split('.')
            pre_answer_pause_s = 0.5 if len(sentences) > 1 else 1.0
            
            # Estimate silence ratio (based on punctuation)
            punctuation_count = len(re.findall(r'[.!?,;:]', text))
            silence_ratio = min(punctuation_count / max(word_count, 1) * 0.1, 0.3)
            
            return {
                "answer_duration_s": estimated_duration_s,
                "pre_answer_pause_s": pre_answer_pause_s,
                "avg_silence_ratio": silence_ratio,
                "speech_rate_wpm": avg_wpm
            }
            
        except Exception as e:
            print(f"Paralinguistic calculation failed: {e}")
            return {
                "answer_duration_s": 0.0,
                "pre_answer_pause_s": 0.0,
                "avg_silence_ratio": 0.0,
                "speech_rate_wpm": 0.0
            }

    def analyze_confidence_indicators(self, text: str) -> Dict[str, float]:
        """Analyze confidence indicators in text"""
        try:
            confidence_indicators = {
                "definite_statements": len(re.findall(r'\b(всегда|никогда|точно|определенно|конечно)\b', text.lower())),
                "hedging_words": len(re.findall(r'\b(возможно|может быть|наверное|вроде|кажется)\b', text.lower())),
                "technical_terms": len(re.findall(r'\b(api|database|framework|algorithm|optimization)\b', text.lower())),
                "specific_examples": len(re.findall(r'\b(например|к примеру|в частности|такой как)\b', text.lower()))
            }
            
            # Calculate confidence score
            total_words = len(text.split())
            if total_words == 0:
                return {"confidence_score": 0.5}
            
            definite_ratio = confidence_indicators["definite_statements"] / total_words
            hedging_ratio = confidence_indicators["hedging_words"] / total_words
            technical_ratio = confidence_indicators["technical_terms"] / total_words
            examples_ratio = confidence_indicators["specific_examples"] / total_words
            
            # Confidence formula
            confidence_score = (
                0.3 * min(definite_ratio * 50, 1.0) +
                0.2 * min(technical_ratio * 20, 1.0) +
                0.3 * min(examples_ratio * 30, 1.0) -
                0.2 * min(hedging_ratio * 40, 1.0)
            )
            
            confidence_score = max(0.0, min(1.0, confidence_score))
            
            return {
                "confidence_score": confidence_score,
                **confidence_indicators
            }
            
        except Exception as e:
            print(f"Confidence analysis failed: {e}")
            return {"confidence_score": 0.5}
