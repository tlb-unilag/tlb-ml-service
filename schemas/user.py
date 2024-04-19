from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    user_id: str = None
    email: str
    country: str
    state: str
    hashed_password: str = None
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        from_attributes = True


class UpdateUser(BaseModel):
    email: str = None
    country: str
    state: str


class UserResponse(BaseModel):
    user_id: str = None
    email: str
    country: str
    state: str
    created_at: datetime = None
    updated_at: datetime = None
