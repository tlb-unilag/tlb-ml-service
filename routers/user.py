from fastapi import Header, APIRouter

from services.auth import *
from services.user import *
from . import version

router = APIRouter(
    prefix=version,
    tags=["user"],
)


@router.get("/user")
async def get_one_user(
        x_api_key: Annotated[str, Header()],
        user: Annotated[User, Depends(get_current_active_user)],
        db: Session = Depends(get_db)
) -> Detection:
    user = read_user(user.user_id, db)
    return user


@router.put("/user")
async def update_a_user(
        x_api_key: Annotated[str, Header()],
        update: UpdateUser,
        user: Annotated[User, Depends(get_current_active_user)],
        db: Session = Depends(get_db)
) -> Detection:
    user = update_user(db, user.user_id, update)
    return user
