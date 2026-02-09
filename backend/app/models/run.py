from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum, Float, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.core.database import Base
import enum

class RunStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class Run(Base):
    __tablename__ = "runs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, nullable=True) # Future-proofing
    
    url = Column(String, nullable=False)
    reference_image_path = Column(String, nullable=True)
    figma_link = Column(String, nullable=True)
    
    status = Column(String, default=RunStatus.PENDING)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Artifacts
    screenshot_path = Column(String, nullable=True)
    diff_image_path = Column(String, nullable=True)
    
    # Results
    issues = Column(JSON, nullable=True) # List of issue objects
    score = Column(Float, nullable=True) # Similarity score

    def __repr__(self):
        return f"<Run(id={self.id}, url={self.url}, status={self.status})>"
