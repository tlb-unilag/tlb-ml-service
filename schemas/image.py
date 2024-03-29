from datetime import datetime

from pydantic import BaseModel


class ImageRequest(BaseModel):
    image_url: str


class Image(BaseModel):
    image_id: str = None
    image_url: str
    location: str
    user_id: str = None
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        from_attributes = True
