import uuid
from fastapi import HTTPException
from sqlalchemy.orm import Session
from schemas.detection import Detection as DetectionSchema, AllDetections
from models.detection import get_detection, get_detections, create_user_detection
from models import Detection as DetectionModel
from schemas.image import ImageRequest
from services.ml import predict, prepare_all_class_count, get_class_frequency


def get_model_detection(image: ImageRequest, model) -> DetectionSchema:
    results, image_url, id = predict(image.image_url, model)
    count = prepare_all_class_count(get_class_frequency(results[0]))
    detection_from_model = DetectionSchema(
        detection_id=id,
        image_url=image_url,
        early=count['early'],
        healthy=count['healthy'],
        not_early=count['not_early'],
    )
    return detection_from_model


def create_new_detection(detection: DetectionSchema, user_id: str, db: Session) -> DetectionModel:
    detection.user_id = user_id
    return create_user_detection(db=db, detection=detection)


def read_detections(user_id: str, db: Session, skip: int = 0, limit: int = 100):
    detections = get_detections(db, user_id=user_id, skip=skip, limit=limit)
    return detections


def read_detection(detection_id: str, db: Session):
    db_detection = get_detection(db, detection_id=detection_id)
    if db_detection is None:
        raise HTTPException(status_code=404, detail="Detection not found")
    return db_detection
