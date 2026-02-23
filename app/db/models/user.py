from sqlalchemy import Column, Integer, DateTime, String
from datetime import datetime
from sqlalchemy.orm import relationship 
from app.db.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    detection_requests = relationship("DetectionRequest",back_populates="user",cascade="all, delete-orphan")
