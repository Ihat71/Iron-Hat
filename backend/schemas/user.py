from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    full_name: str
    username: str = Field(min_length = 3, max_length = 20)
    email: EmailStr
    gender: str

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    created_at: datetime
    last_updated_username: datetime

class UserUpdate(BaseModel):
    full_name: str | None = None
    username: str | None = None
    email: EmailStr | None = None
    last_updated_username: datetime | None = None

class UserNameUpdate(BaseModel):
    username: str
    last_updated_username: datetime

class UserEmailUpdate(BaseModel):
    email: EmailStr

class UserFullNameUpdate(BaseModel):
    full_name: str


class UserLogin(BaseModel):
    username: str
    email: EmailStr | None = None
    password: str