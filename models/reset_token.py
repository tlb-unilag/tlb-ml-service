from sqlalchemy.orm import Session

from models import ResetToken
from schemas.auth import ResetToken as ResetTokenSchema


def get_token_by_user_id(db: Session, user_id: str):
    return db.query(ResetToken).filter(ResetToken.user_id == user_id).first()


def create_reset_token(db: Session, reset_token: ResetTokenSchema):
    db_item = ResetToken(**reset_token.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_token(db: Session, user_id: str):
    token = db.query(ResetToken).filter(ResetToken.user_id == user_id).first()
    if token:
        db.delete(token)
        db.commit()
        return True
    else:
        return False
