from sqlalchemy.orm import Session

from models import Detection
from schemas.detection import Detection as DetectionSchema


def get_detection(db: Session, detection_id: str):
    return db.query(Detection).filter(Detection.detection_id == detection_id).first()


def get_detections(db: Session, user_id: str, skip: int = 0, limit: int = 100):
    return db.query(Detection).filter(Detection.user_id == user_id).offset(skip).limit(limit).all()


def create_user_detection(db: Session, detection: DetectionSchema):
    db_item = Detection(**detection.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
