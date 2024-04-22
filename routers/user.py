from fastapi import APIRouter, Request

from database import get_db
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
        token: Annotated[str, Depends(oauth2_scheme)],
        db: Session = Depends(get_db)
) -> UserResponse:
    user = get_current_active_user(db, token)
    user = read_user(db, user.user_id)
    return user


@router.put("/user")
@limiter.limit("100/minute")
async def update_user(
        request: Request,
        update: UpdateUser,
        token: Annotated[str, Depends(oauth2_scheme)],
        db: Session = Depends(get_db)
) -> UserResponse:
    user = get_current_active_user(db, token)
    if update.email is None:
        update.email = user.email
    if user.email == update.email:
        user = update_one_user(db, user.user_id, update)
        return user
    else:
        existing_user = read_user_by_email(db, update.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User email exists.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        else:
            user = update_one_user(db, user.user_id, update)
            return user
