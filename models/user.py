from sqlalchemy.orm import Session

from models import User
from schemas.user import User as UserSchema


def get_user(db: Session, user_id: str):
    return db.query(User).filter(User.user_id == user_id).first()


def update_user(db: Session, user_id: str, update: UserSchema):
    user: User = db.query(User).filter(User.user_id == user_id).first()
    if user:
        user.email = update.email
        user.country = update.country
        user.state = update.state
    db.commit()
    db.refresh(user)
    return user


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserSchema):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
