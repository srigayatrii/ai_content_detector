from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime
from app.db.database import Base


class DetectionRequest(Base):
    __tablename__ = "detection_requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    text = Column(Text, nullable=False)
    input_length = Column(Integer, nullable=False)
    model_used = Column(String, nullable=False)
    status = Column(String, nullable=False, default="processing")

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)