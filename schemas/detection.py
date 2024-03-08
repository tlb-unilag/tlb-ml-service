from datetime import datetime
from typing import List

from pydantic import BaseModel


class Detection(BaseModel):
    detection_id: str = None
    image_url: str
    early: int
    healthy: int
    not_early: int
    user_id: str = None
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True


class AllDetections(BaseModel):
    detections: List[Detection]
