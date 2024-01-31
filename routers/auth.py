from fastapi import Header, APIRouter

from services.auth import *
from services.user import *
from . import version

router = APIRouter(
    prefix=version,
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


@router.post("/login")
async def login(
        login_details: Login,
        x_api_key: Annotated[str, Header()] = None,
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
async def signup(
        signup_details: Signup,
        x_api_key: Annotated[str, Header()] = None,
        db: Session = Depends(get_db)
) -> Token:
    hashed_passwd = get_password_hash(signup_details.password)
    user = create_new_user(signup_details, hashed_passwd, db)
    if user is None:
        raise HTTPException(status_code=400, detail="Unable to create new user")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
