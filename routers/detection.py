from fastapi import Header, APIRouter

from services.auth import *
from services.detection import *
from . import version

router = APIRouter(
    prefix=version,
    tags=["detection"],
)


@router.post("/detection")
async def make_one_detection(
        image_data: ImageRequest,
        x_api_key: Annotated[str, Header()],
        user: Annotated[User, Depends(get_current_active_user)],
        db: Session = Depends(get_db)
) -> Detection:
    detection_from_model = get_model_detection(image_data)
    detection = create_new_detection(detection_from_model, user.user_id, db)
    return detection


@router.get("/detection/{detection_id}")
async def get_one_detection(
        detection_id: str,
        x_api_key: Annotated[str, Header()],
        user: Annotated[User, Depends(get_current_active_user)],
        db: Session = Depends(get_db)
) -> Detection:
    detection = read_detection(detection_id, db)
    return detection


@router.get("/detection")
async def get_all_detections(
        x_api_key: Annotated[str, Header()],
        user: Annotated[User, Depends(get_current_active_user)],
        db: Session = Depends(get_db)
):
    all_detections = read_detections(user.user_id, db)
    return {"detections": all_detections}
