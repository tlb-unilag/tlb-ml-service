from datetime import datetime
from typing import List

from pydantic import BaseModel


class Detection(BaseModel):
    detection_id: str = None
    image_url: str
    early: int
    healthy: int
    not_early: int
    image_id: str = None
    user_id: str = None
    solution: str = None
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        from_attributes = True


class AllDetections(BaseModel):
    detections: List[Detection]
