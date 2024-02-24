from fastapi import Header, APIRouter
from ultralytics.nn.tasks import DetectionModel as YoloDetectionModel

from services.auth import *
from services.detection import *
from services.ml import get_detection_model
from . import version

router = APIRouter(
    prefix=version,
    tags=["detection"],
)


@router.post("/detection")
async def make_one_detection(
        image_data: ImageRequest,
        user: Annotated[User, Depends(get_current_active_user)],
        model: Annotated[YoloDetectionModel, Depends(get_detection_model)],
        db: Session = Depends(get_db)
) -> Detection:
    detection_from_model = get_model_detection(image_data, model)
    detection = create_new_detection(detection_from_model, user.user_id, db)
    return detection


@router.get("/detection/{detection_id}")
async def get_one_detection(
        detection_id: str,
        user: Annotated[User, Depends(get_current_active_user)],
        db: Session = Depends(get_db)
) -> Detection:
    detection = read_detection(detection_id, db)
    return detection


@router.get("/detection")
async def get_all_detections(
        user: Annotated[User, Depends(get_current_active_user)],
        db: Session = Depends(get_db)
):
    all_detections = read_detections(user.user_id, db)
    return {"detections": all_detections}
