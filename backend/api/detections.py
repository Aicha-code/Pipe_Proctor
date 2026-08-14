from __future__ import annotations

from datetime import datetime, timezone
from typing import Annotated, Literal, Optional
from uuid import uuid4

from fastapi import APIRouter, HTTPException, Query, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field, field_validator


AnomalyType = Literal["oil_spill", "land_excavation", "fire_outbreak"]
AnomalyStatus = Literal["detected", "investigating", "resolved"]


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


class DetectionCreate(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    anomaly_type: AnomalyType
    confidence: float = Field(..., ge=0.0, le=1.0)
    detected_at: datetime
    image_id: str = Field(..., min_length=1)

    @field_validator("detected_at")
    @classmethod
    def validate_detected_at(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value


class DetectionUpdateStatus(BaseModel):
    anomaly_status: AnomalyStatus


class DetectionRecord(BaseModel):
    id: str
    latitude: float
    longitude: float
    anomaly_type: AnomalyType
    anomaly_status: AnomalyStatus = "detected"
    confidence: float
    detected_at: datetime
    image_id: str
    created_at: datetime
    updated_at: datetime


class NotificationEvent(BaseModel):
    event: str = "new_anomaly"
    detection_id: str
    latitude: float
    longitude: float
    anomaly_type: AnomalyType
    anomaly_status: AnomalyStatus
    confidence: float


_detection_store: dict[str, DetectionRecord] = {}


def _make_detection_record(payload: DetectionCreate) -> DetectionRecord:
    now = _utc_now()
    return DetectionRecord(
        id=str(uuid4()),
        latitude=payload.latitude,
        longitude=payload.longitude,
        anomaly_type=payload.anomaly_type,
        anomaly_status="detected",
        confidence=payload.confidence,
        detected_at=payload.detected_at,
        image_id=payload.image_id,
        created_at=now,
        updated_at=now,
    )


detection_router = APIRouter(prefix="/api/v1", tags=["Detections"])


@detection_router.post(
    "/detections",
    response_model=DetectionRecord,
    status_code=status.HTTP_201_CREATED,
    summary="Submit a new anomaly detection",
)
def create_detection(payload: DetectionCreate):
    """Create a detection record from the ML detection service."""
    record = _make_detection_record(payload)
    _detection_store[record.id] = record
    return record


@detection_router.get(
    "/detections",
    response_model=list[DetectionRecord],
    summary="List detections with optional filters",
)
def list_detections(
    anomaly_type: Optional[AnomalyType] = Query(default=None),
    anomaly_status: Optional[AnomalyStatus] = Query(default=None),
    latitude: Optional[float] = Query(default=None, ge=-90, le=90),
    longitude: Optional[float] = Query(default=None, ge=-180, le=180),
    from_date: Optional[datetime] = Query(default=None, alias="from_date"),
    to_date: Optional[datetime] = Query(default=None, alias="to_date"),
):
    """Return detections that can be filtered by anomaly type, status, and time/location."""
    detections = list(_detection_store.values())

    if anomaly_type is not None:
        detections = [item for item in detections if item.anomaly_type == anomaly_type]
    if anomaly_status is not None:
        detections = [item for item in detections if item.anomaly_status == anomaly_status]
    if latitude is not None:
        detections = [item for item in detections if abs(item.latitude - latitude) <= 0.0001]
    if longitude is not None:
        detections = [item for item in detections if abs(item.longitude - longitude) <= 0.0001]
    if from_date is not None:
        detections = [item for item in detections if item.detected_at >= from_date]
    if to_date is not None:
        detections = [item for item in detections if item.detected_at <= to_date]

    return sorted(detections, key=lambda item: item.detected_at, reverse=True)


@detection_router.get(
    "/detections/{detection_id}",
    response_model=DetectionRecord,
    summary="Get a detection by ID",
)
def get_detection(detection_id: str):
    detection = _detection_store.get(detection_id)
    if detection is None:
        raise HTTPException(status_code=404, detail="Detection not found")
    return detection


@detection_router.patch(
    "/detections/{detection_id}/status",
    response_model=DetectionRecord,
    summary="Update the anomaly status",
)
def update_detection_status(detection_id: str, payload: DetectionUpdateStatus):
    detection = _detection_store.get(detection_id)
    if detection is None:
        raise HTTPException(status_code=404, detail="Detection not found")

    detection.anomaly_status = payload.anomaly_status
    detection.updated_at = _utc_now()
    _detection_store[detection_id] = detection
    return detection


@detection_router.get(
    "/notifications/stream",
    summary="Stream dashboard notifications as SSE",
    response_class=StreamingResponse,
)
def stream_notifications():
    """Server-Sent Events endpoint for dashboard updates.

    SSE is preferable here because notifications are one-way, low-volume, and naturally
    broadcast to multiple dashboard clients with automatic reconnect behavior.
    """

    def event_generator():
        for detection in _detection_store.values():
            event = NotificationEvent(
                detection_id=detection.id,
                latitude=detection.latitude,
                longitude=detection.longitude,
                anomaly_type=detection.anomaly_type,
                anomaly_status=detection.anomaly_status,
                confidence=detection.confidence,
            )
            yield f"event: new_anomaly\ndata: {event.model_dump_json()}\n\n"
            break

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )
