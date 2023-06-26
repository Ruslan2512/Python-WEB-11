from datetime import datetime

from pydantic import BaseModel, Field, EmailStr

from src.database.models import Role


class ContactModel(BaseModel):
    fullname: str = Field(min_length=3, max_length=16)
    lastname: str = Field(min_length=3, max_length=16)
    email: EmailStr
    phone_number: str = Field(min_length=3, max_length=16)
    birthday: str = Field(min_length=3, max_length=16)


class ContactResponse(BaseModel):
    fullname: str
    lastname: str
    email: EmailStr
    phone_number: str
    birthday: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class UserModel(BaseModel):
    username: str = Field(min_length=6, max_length=12)
    email: EmailStr
    password: str = Field(min_length=6, max_length=8)


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    avatar: str
    roles: Role

    class Config:
        orm_mode = True


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
