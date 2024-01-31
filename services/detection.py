import uuid
from fastapi import HTTPException
from sqlalchemy.orm import Session
from schemas.detection import Detection as DetectionSchema, AllDetections
from models.detection import get_detection, get_detections, create_user_detection
from models import Detection as DetectionModel
from schemas.image import ImageRequest


def get_model_detection(image: ImageRequest) -> DetectionSchema:
    detection_from_model = DetectionSchema(
        image_url=image.image_url,
        taro_late=2,
        taro_mid=4,
        taro_early=9,
    )
    return detection_from_model


def create_new_detection(detection: DetectionSchema, user_id: str, db: Session) -> DetectionModel:
    detection.user_id = user_id
    detection.detection_id = str(uuid.uuid4())
    return create_user_detection(db=db, detection=detection)


def read_detections(user_id: str, db: Session, skip: int = 0, limit: int = 100):
    detections = get_detections(db, user_id=user_id, skip=skip, limit=limit)
    return detections


def read_detection(detection_id: str, db: Session):
    db_detection = get_detection(db, detection_id=detection_id)
    if db_detection is None:
        raise HTTPException(status_code=404, detail="Detection not found")
    return db_detection
