from typing import Annotated

from fastapi import APIRouter, Depends, Request
from ultralytics.nn.tasks import DetectionModel as YoloDetectionModel
from sqlalchemy.orm import Session

from database import get_db
from schemas.detection import Detection
from services.auth import get_current_active_user, oauth2_scheme
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
        model: Annotated[YoloDetectionModel, Depends(get_detection_model)],
        token: Annotated[str, Depends(oauth2_scheme)],
        db: Session = Depends(get_db),
) -> Detection:
    user = get_current_active_user(db, token)
    image = create_new_image(db, image_data, user_id=user.user_id, location=user.state)
    detection_from_model = get_model_detection(image, model)
    detection = create_new_detection(db, detection_from_model, image.image_id, user.user_id)
    return detection


@router.get("/detection/{detection_id}")
@limiter.limit("100/minute")
async def get_one_detection(
        request: Request,
        detection_id: str,
        token: Annotated[str, Depends(oauth2_scheme)],
        db: Session = Depends(get_db)
):
    _user = get_current_active_user(db, token)
    detection = read_detection(db, detection_id)
    return detection


@router.get("/detection")
@limiter.limit("100/minute")
async def get_all_detections(
        request: Request,
        token: Annotated[str, Depends(oauth2_scheme)],
        db: Session = Depends(get_db)
):
    user = get_current_active_user(db, token)
    all_detections = read_detections(db, user.user_id)
    return {"detections": all_detections}
