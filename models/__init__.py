from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from database import Base
from typing import List


class Image(Base):
    __tablename__ = "image"

    image_id = Column(String, primary_key=True, index=True)
    image_url = Column(String, index=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())

    user_id = mapped_column(String, ForeignKey("user.user_id"))
    user: Mapped["User"] = relationship(back_populates="images")


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
    user: Mapped["User"] = relationship(back_populates="detections")


# ToDo: Check is active status
class User(Base):
    __tablename__ = "user"

    user_id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    country = Column(String, index=True)
    state = Column(String, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())

    detections: Mapped[List["Detection"]] = relationship(
        back_populates="user", cascade="all, delete-orphan")
    images: Mapped[List["Image"]] = relationship(
        back_populates="user", cascade="all, delete-orphan")
