from typing import Union
from datetime import datetime

from pydantic import BaseModel, Field


class Signup(BaseModel):
    email: str = Field(
        title="user email", min_length=5
    )
    password: str = Field(
        title="user password", min_length=5
    )
    country: str = Field(
        title="country of current location", min_length=5
    )
    state: str = Field(
        title="state of current location", min_length=5
    )


class Login(BaseModel):
    email: str = Field(
        title="user email", min_length=5
    )
    password: str = Field(
        title="user password", min_length=5
    )


class LoginResponse(BaseModel):
    user_id: str
    token: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Union[str, None] = None


class ForgotPassword(BaseModel):
    email: Union[str, None] = None


class ResetPassword(BaseModel):
    email: Union[str, None] = None
    reset_token: Union[str, None] = None
    new_password: Union[str, None] = None


class ResetToken(BaseModel):
    id: str = None
    hashed_password: str = None
    user_id: str = None
    created_at: datetime = None

    class Config:
        from_attributes = True
