from fastapi import APIRouter, Request

from database import get_db
from services.auth import *
from services.email import EmailClient
from services.reset_token import create_new_reset_token, authenticate_token, delete_reset_token
from services.user import *
from services.util import limiter
from . import version

router = APIRouter(
    prefix=version,
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


@router.post("/login")
@limiter.limit("100/minute")
async def login(
        request: Request,
        login_details: Login,
        db: Session = Depends(get_db)
) -> Token:
    user = authenticate_user(db, login_details.email, login_details.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post("/signup", status_code=201)
@limiter.limit("100/minute")
async def signup(
        request: Request,
        signup_details: Signup,
        db: Session = Depends(get_db)
) -> Token:
    user = create_new_user(signup_details, db)
    if user is None:
        raise HTTPException(status_code=400, detail="Unable to create new user")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post("/forgot-password", status_code=201)
@limiter.limit("100/minute")
async def forgot_password(
        request: Request,
        user_data: ForgotPassword,
        db: Session = Depends(get_db)
):
    user = read_user_by_email(db, user_data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    secret = generate_secret()
    reset_token = create_new_reset_token(db, user.user_id, secret)
    if reset_token:
        client = EmailClient()
        res = client.send_mail(user.email, secret)
        if not res:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error sending reset token.",
                headers={"WWW-Authenticate": "Bearer"},
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating reset token.",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/reset-password")
@limiter.limit("100/minute")
async def reset_password(
        request: Request,
        reset_data: ResetPassword,
        db: Session = Depends(get_db)
) -> Token:
    user = read_user_by_email(db, reset_data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = authenticate_token(db, user.user_id, reset_data.reset_token)
    if token:
        user = update_user_password(db, user.user_id, reset_data.new_password)
        if user is None:
            raise HTTPException(status_code=400, detail="Error updating user password")
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        delete_reset_token(db, user.user_id)
        return Token(access_token=access_token, token_type="bearer")
    else:
        raise HTTPException(status_code=400, detail="Error authenticating reset token")
