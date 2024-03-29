import uuid
from fastapi import Depends, HTTPException
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database import get_db
from models import ResetToken
from schemas.auth import ResetToken as ResetTokenSchema
from models.reset_token import create_reset_token, get_token_by_user_id, delete_token
from services.auth import RESET_TOKEN_EXPIRE_MINUTES
from services.util import verify_password, get_password_hash


def create_new_reset_token(user_id: str, secret: str, db: Session = Depends(get_db)) -> ResetToken:
    token = read_reset_token_by_user_id(user_id, db=db)
    if token:
        delete_token(db, user_id)
    uuid_v4 = str(uuid.uuid4())
    hp = get_password_hash(secret)
    return create_reset_token(db=db, reset_token=ResetTokenSchema(id=uuid_v4, user_id=user_id, hashed_password=hp))


def read_reset_token_by_user_id(user_id: str, db: Session = Depends(get_db)):
    token = get_token_by_user_id(db, user_id=user_id)
    return token


def delete_reset_token(user_id: str, db: Session = Depends(get_db)):
    return delete_token(db, user_id)


def authenticate_token(user_id: str, password: str, db: Session = Depends(get_db)):
    token = read_reset_token_by_user_id(user_id, db=db)
    if not token:
        raise HTTPException(status_code=404, detail="User reset token not found")

    if not verify_password(password, token.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid reset token")
    expiration_threshold = timedelta(minutes=RESET_TOKEN_EXPIRE_MINUTES)
    if token.created_at + expiration_threshold < datetime.utcnow():
        delete_token(db, user_id)
        raise HTTPException(status_code=401, detail="Reset token expired")
    return token
