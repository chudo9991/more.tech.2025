"""
Message model for chat messages
"""
from sqlalchemy import Column, String, Integer, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Message(Base):
    __tablename__ = "messages"
    
    id = Column(String, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("sessions.id"), nullable=False)
    text = Column(Text, nullable=False)
    message_type = Column(String, nullable=False)  # 'user' or 'avatar'
    audio_url = Column(String, nullable=True)  # MinIO URL for audio file
    transcription_confidence = Column(Integer, nullable=True)  # Whisper confidence
    tone_analysis = Column(String, nullable=True)  # Tone analysis result
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    session = relationship("Session", back_populates="messages")
