from datetime import datetime

from pydantic import BaseModel
from schemas.detection import Detection
from schemas.image import Image


class User(BaseModel):
    user_id: str = None
    email: str
    country: str
    state: str
    hashed_password: str = None
    created_at: datetime = None
    updated_at: datetime = None
    detections: list[Detection] = []
    images: list[Image] = []

    class Config:
        orm_mode = True


class UpdateUser(BaseModel):
    country: str
    state: str
