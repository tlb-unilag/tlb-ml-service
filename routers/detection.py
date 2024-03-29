from typing import Annotated

from fastapi import APIRouter, Depends, Request
from ultralytics.nn.tasks import DetectionModel as YoloDetectionModel
from sqlalchemy.orm import Session

from database import get_db
from schemas.detection import Detection
from schemas.user import User
from services.auth import get_current_active_user
from services.detection import create_new_detection, read_detection, read_detections, get_model_detection
from schemas.image import ImageRequest
from services.image import create_new_image
from services.ml import get_detection_model
from services.util import limiter
from . import version

router = APIRouter(
    prefix=version,
    tags=["detection"],
)


@router.post("/detection")
@limiter.limit("100/minute")
async def make_one_detection(
        request: Request,
        image_data: ImageRequest,
        user: Annotated[User, Depends(get_current_active_user)],
        model: Annotated[YoloDetectionModel, Depends(get_detection_model)],
        db: Session = Depends(get_db)
) -> Detection:
    image = create_new_image(image_data, user_id=user.user_id, db=db, location=user.state)
    detection_from_model = get_model_detection(image, model)
    detection = create_new_detection(detection_from_model, user.user_id, db)
    return detection


@router.get("/detection/{detection_id}")
@limiter.limit("100/minute")
async def get_one_detection(
        request: Request,
        detection_id: str,
        user: Annotated[User, Depends(get_current_active_user)],
        db: Session = Depends(get_db)
) -> Detection:
    detection = read_detection(detection_id, db)
    return detection


@router.get("/detection")
@limiter.limit("100/minute")
async def get_all_detections(
        request: Request,
        user: Annotated[User, Depends(get_current_active_user)],
        db: Session = Depends(get_db)
):
    all_detections = read_detections(user.user_id, db)
    return {"detections": all_detections}
