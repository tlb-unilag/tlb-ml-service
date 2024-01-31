import uuid
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.image import Image as ImageSchema, ImageRequest
from database import get_db
from models.image import get_image, get_images, create_user_image
from models import Image as ImageModel


def create_new_image(image: ImageRequest, user_id: str, db: Session = Depends(get_db)) -> ImageModel:
    uuid_v4 = str(uuid.uuid4())
    return create_user_image(db=db, image=ImageSchema(**image.dict(), image_id=uuid_v4, user_id=user_id))


def read_images(user_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    images = get_images(db, user_id=user_id, skip=skip, limit=limit)
    return images


def read_image(image_id: str, db: Session = Depends(get_db)):
    db_image = get_image(db, image_id=image_id)
    if db_image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return db_image
