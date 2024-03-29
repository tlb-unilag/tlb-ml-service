from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import mapped_column
from database import Base
from sqlalchemy import event


class Image(Base):
    __tablename__ = "image"

    image_id = Column(String, primary_key=True, index=True)
    image_url = Column(String, index=True)
    location = Column(String, index=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())

    user_id = mapped_column(String, ForeignKey("user.user_id"))


class Detection(Base):
    __tablename__ = "detection"

    detection_id = Column(String, primary_key=True, index=True)
    image_url = Column(String, index=True)
    early = Column(Integer, index=True)
    healthy = Column(Integer, index=True)
    not_early = Column(Integer, index=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())

    user_id = mapped_column(String, ForeignKey("user.user_id"))


class User(Base):
    __tablename__ = "user"

    user_id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    country = Column(String, index=True)
    state = Column(String, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())


class ResetToken(Base):
    __tablename__ = "reset_token"

    id = Column(String, primary_key=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=func.now())
    user_id = mapped_column(String, ForeignKey("user.user_id"))


@event.listens_for(Image, 'before_update')
def update_timestamps_before_update(mapper, connection, target):
    target.updated_at = func.now()


@event.listens_for(Detection, 'before_update')
def update_timestamps_before_update(mapper, connection, target):
    target.updated_at = func.now()


@event.listens_for(User, 'before_update')
def update_timestamps_before_update(mapper, connection, target):
    target.updated_at = func.now()
