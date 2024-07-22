from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from models import Image
from schemas.image import Image as ImageSchema


def get_image(db: Session, image_id: str):
    return db.query(Image).filter(Image.image_id == image_id).first()


def get_image_at_created_at(db: Session, created_at: datetime, delta: int):
    start_time = created_at - timedelta(seconds=delta)
    end_time = created_at + timedelta(seconds=delta)
    return db.query(Image).filter(Image.created_at.between(start_time, end_time)).first()


def get_image_with_url(db: Session, image_url: str):
    return db.query(Image).filter(Image.image_url == image_url).first()


def get_images(db: Session, user_id: str, skip: int = 0, limit: int = 100):
    return db.query(Image).filter(Image.user_id == user_id).offset(skip).limit(limit).all()


def create_user_image(db: Session, image: ImageSchema):
    db_item = Image(**image.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
