from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from app.db.database import Base


class DetectionResult(Base):
    __tablename__ = "detection_results"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(
        Integer,
        ForeignKey("detection_requests.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    ai_probability = Column(Float, nullable=False)
    metrics = Column(JSONB, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)