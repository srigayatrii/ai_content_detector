import random
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.core.security import get_current_user
from app.db.models.detection_request import DetectionRequest
from app.db.models.detection_result import DetectionResult
from app.schemas.detection import DetectionResultResponse, DetectionRequestCreate
from app.db.models.user import User

router = APIRouter(prefix="/detect", tags=["Detection"])


@router.post("/", response_model=DetectionResultResponse)
def detect_ai_content(
    payload: DetectionRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1. Calculate input length
    input_length = len(payload.text)

    # 2. Create detection request
    detection_request = DetectionRequest(
        user_id=current_user.id,
        text=payload.text,
        input_length=input_length,
        model_used="mock-ai-detector-v1",
        status="processing"
    )
    db.add(detection_request)
    db.commit()
    db.refresh(detection_request)

    # 3. Mock AI logic
    ai_probability = round(random.uniform(0.1, 0.95), 2)

    metrics_data = {
        "confidence": round(random.uniform(0.6, 0.99), 2),
        "risk_level": (
            "High" if ai_probability > 0.7
            else "Medium" if ai_probability > 0.4
            else "Low"
        ),
        "sentence_count": len(payload.text.split(".")),
        "model": "mock-ai-detector-v1"
    }

    # 4. Store result
    detection_result = DetectionResult(
        request_id=detection_request.id,
        ai_probability=ai_probability,
        metrics=metrics_data
    )
    db.add(detection_result)

    # 5. Update status
    detection_request.status = "completed"
    db.commit()
    db.refresh(detection_result)

    # 6. RETURN CORRECT SCHEMA (RESULT, not request)
    return DetectionResultResponse(
        id=detection_result.id,
        request_id=detection_result.request_id,
        ai_probability=detection_result.ai_probability,
        metrics=detection_result.metrics,
        created_at=detection_result.created_at
    )


@router.get("/history", response_model=List[DetectionResultResponse])
def get_detection_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Get all detection requests for this user (latest first)
    requests = (
        db.query(DetectionRequest)
        .filter(DetectionRequest.user_id == current_user.id)
        .order_by(DetectionRequest.id.desc())
        .all()
    )

    history = []

    for req in requests:
        result = (
            db.query(DetectionResult)
            .filter(DetectionResult.request_id == req.id)
            .first()
        )

        if result:
            history.append(
                DetectionResultResponse(
                    id=result.id,
                    request_id=result.request_id,
                    ai_probability=result.ai_probability,
                    metrics=result.metrics,
                    created_at=result.created_at
                )
            )

    return history




@router.get("/{request_id}", response_model=DetectionResultResponse)
def get_detection_by_id(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1. Get the detection request
    detection_request = (
        db.query(DetectionRequest)
        .filter(DetectionRequest.id == request_id)
        .first()
    )

    # 2. If request does not exist
    if not detection_request:
        raise HTTPException(status_code=404, detail="Detection request not found")

    # 3. SECURITY CHECK (CRITICAL)
    # Prevent users from accessing other users' detections
    if detection_request.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this detection")

    # 4. Get the result linked to this request
    detection_result = (
        db.query(DetectionResult)
        .filter(DetectionResult.request_id == request_id)
        .first()
    )

    if not detection_result:
        raise HTTPException(status_code=404, detail="Detection result not found")

    # 5. Return proper response schema
    return DetectionResultResponse(
        id=detection_result.id,
        request_id=detection_result.request_id,
        ai_probability=detection_result.ai_probability,
        metrics=detection_result.metrics,
        created_at=detection_result.created_at
    )