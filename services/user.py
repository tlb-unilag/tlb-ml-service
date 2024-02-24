import uuid
from fastapi import HTTPException
from sqlalchemy.orm import Session
from schemas.user import User as UserSchema, UpdateUser
from schemas.auth import Signup
from models.user import get_user, get_users, get_user_by_email, create_user
from models import User as UserModel
from services.util import get_password_hash


def create_new_user(user: Signup, db: Session) -> UserModel:
    hashed_passwd = get_password_hash(user.password)
    uuid_v4 = str(uuid.uuid4())
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, user=UserSchema(**user.dict(), user_id=uuid_v4, hashed_password=hashed_passwd))


def update_user(db: Session, user_id: str, update: UpdateUser):
    user = update_user(db, user_id, update)
    return user


def read_users(db: Session, skip: int = 0, limit: int = 100):
    users = get_users(db, skip=skip, limit=limit)
    return users


def read_user(user_id: str, db: Session):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


def read_user_by_email(email: str, db: Session):
    db_user = get_user_by_email(db, email=email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
