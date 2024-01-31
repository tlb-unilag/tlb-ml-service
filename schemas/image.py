from datetime import datetime

from pydantic import BaseModel


class ImageRequest(BaseModel):
    image_url: str


class Image(BaseModel):
    image_id: str = None
    image_url: str
    user_id: int = None
    created_at: datetime = None

    class Config:
        orm_mode = True
