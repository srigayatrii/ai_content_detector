from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Any


class DetectionRequestCreate(BaseModel):
    text: str
    model_used: str


class DetectionRequestResponse(BaseModel):
    id: int
    user_id: int
    text: str
    input_length: int
    model_used: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class DetectionResultResponse(BaseModel):
    id: int
    request_id: int
    ai_probability: float
    metrics: Dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True