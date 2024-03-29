from fastapi import APIRouter, Request

from services.auth import *
from services.user import *
from services.util import limiter
from . import version

router = APIRouter(
    prefix=version,
    tags=["user"],
)


@router.get("/user")
@limiter.limit("100/minute")
async def get_user(
        request: Request,
        user: Annotated[User, Depends(get_current_active_user)],
        db: Session = Depends(get_db)
) -> UserResponse:
    user = read_user(user.user_id, db)
    return user


@router.put("/user")
@limiter.limit("100/minute")
async def update_user(
        request: Request,
        update: UpdateUser,
        user: Annotated[User, Depends(get_current_active_user)],
        db: Session = Depends(get_db)
) -> UserResponse:
    user = update_one_user(db, user.user_id, update)
    return user
