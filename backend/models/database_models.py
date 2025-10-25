"""
Database Models - SQLAlchemy ORM
Defines tables for prompts, outputs, feedback, and user profiles
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class UserProfile(Base):
    """User profiles for tracking individual users (optional)"""
    __tablename__ = 'user_profiles'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    total_generations = Column(Integer, default=0)
    
    # Relationships
    prompts = relationship("Prompt", back_populates="user")
    feedbacks = relationship("Feedback", back_populates="user")
    
    def __repr__(self):
        return f"<UserProfile(id={self.id}, username='{self.username}')>"


class Prompt(Base):
    """Stores user prompts and metadata"""
    __tablename__ = 'prompts'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user_profiles.id'), nullable=True)
    prompt_text = Column(Text, nullable=False)
    detected_language = Column(String(50), nullable=True)
    requested_language = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    session_id = Column(String(100), nullable=True)
    
    # Relationships
    user = relationship("UserProfile", back_populates="prompts")
    outputs = relationship("ModelOutput", back_populates="prompt")
    
    def __repr__(self):
        return f"<Prompt(id={self.id}, language='{self.detected_language}')>"


class ModelOutput(Base):
    """Stores generated code outputs from Ollama"""
    __tablename__ = 'model_outputs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    prompt_id = Column(Integer, ForeignKey('prompts.id'), nullable=False)
    model_name = Column(String(100), nullable=False)  # e.g., mistral:latest
    generated_code = Column(Text, nullable=False)
    raw_output = Column(Text, nullable=True)  # Before extraction
    language = Column(String(50), nullable=False)
    generation_time_ms = Column(Integer, nullable=True)  # Time taken to generate
    tokens_used = Column(Integer, nullable=True)
    temperature = Column(Float, default=0.3)
    created_at = Column(DateTime, default=datetime.utcnow)
    success = Column(Boolean, default=True)
    error_message = Column(Text, nullable=True)
    
    # Relationships
    prompt = relationship("Prompt", back_populates="outputs")
    feedback = relationship("Feedback", back_populates="output", uselist=False)
    
    def __repr__(self):
        return f"<ModelOutput(id={self.id}, model='{self.model_name}', language='{self.language}')>"


class Feedback(Base):
    """Stores user feedback on generated code"""
    __tablename__ = 'feedback'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    output_id = Column(Integer, ForeignKey('model_outputs.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user_profiles.id'), nullable=True)
    rating = Column(Integer, nullable=False)  # 1-5 stars
    feedback_type = Column(String(20), nullable=True)  # 'positive', 'negative', 'neutral'
    comments = Column(Text, nullable=True)
    issues_reported = Column(Text, nullable=True)  # JSON string of specific issues
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Learning metrics
    code_quality_score = Column(Float, nullable=True)
    correctness_score = Column(Float, nullable=True)
    efficiency_score = Column(Float, nullable=True)
    
    # Relationships
    output = relationship("ModelOutput", back_populates="feedback")
    user = relationship("UserProfile", back_populates="feedbacks")
    
    def __repr__(self):
        return f"<Feedback(id={self.id}, rating={self.rating}, type='{self.feedback_type}')>"


class LearningPattern(Base):
    """Stores learned patterns from feedback for improvement"""
    __tablename__ = 'learning_patterns'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    language = Column(String(50), nullable=False)
    pattern_type = Column(String(50), nullable=False)  # 'successful', 'failed', 'improvement'
    pattern_description = Column(Text, nullable=False)
    prompt_keywords = Column(Text, nullable=True)  # JSON array
    code_snippet = Column(Text, nullable=True)
    avg_rating = Column(Float, nullable=True)
    occurrence_count = Column(Integer, default=1)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    confidence_score = Column(Float, default=0.5)
    
    def __repr__(self):
        return f"<LearningPattern(id={self.id}, language='{self.language}', type='{self.pattern_type}')>"


class SystemMetrics(Base):
    """Tracks system-wide metrics and performance"""
    __tablename__ = 'system_metrics'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    metric_name = Column(String(100), nullable=False)
    metric_value = Column(Float, nullable=False)
    metric_unit = Column(String(50), nullable=True)
    recorded_at = Column(DateTime, default=datetime.utcnow)
    meta_info = Column(Text, nullable=True)  # JSON string (renamed from metadata)
    
    def __repr__(self):
        return f"<SystemMetrics(metric='{self.metric_name}', value={self.metric_value})>"
