"""
Media model for audio files
"""
from sqlalchemy import Column, Integer, String, BigInteger, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Media(Base):
    __tablename__ = "media"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(50), ForeignKey("sessions.id"), nullable=False)
    kind = Column(String(50), nullable=False)  # 'question_audio', 'answer_audio'
    url = Column(String(500), nullable=False)
    duration_ms = Column(Integer)
    file_size_bytes = Column(BigInteger)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    session = relationship("Session", back_populates="media_files")
