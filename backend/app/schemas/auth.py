from pydantic import BaseModel, EmailStr
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[str] = None
    email: Optional[str] = None
    roles: list[str] = []


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: str = "HOSPITAL_ADMIN"
    hospital_id: Optional[str] = None


class UserRead(BaseModel):
    id: str
    email: EmailStr
    full_name: str
    role: str
    hospital_id: Optional[str] = None
    is_active: bool

    class Config:
        from_attributes = True
