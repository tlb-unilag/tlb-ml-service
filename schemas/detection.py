from datetime import datetime
from typing import List

from pydantic import BaseModel


class Count(BaseModel):
    taro_late: int
    taro_mid: int
    taro_early: int


class Detection(BaseModel):
    detection_id: str = None
    image_url: str
    taro_late: int
    taro_mid: int
    taro_early: int
    taro_healthy: int
    user_id: str = None
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True


class AllDetections(BaseModel):
    detections: List[Detection]
