from datetime import datetime

from pydantic import BaseModel, Field, EmailStr


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
