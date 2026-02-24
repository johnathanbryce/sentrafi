from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional


# client sends to /register:
class UserCreate(BaseModel):
    email: EmailStr
    password: str


# client sends to /login:
class UserLogin(BaseModel):
    email: Optional[EmailStr]
    username: Optional[str]
    password: str


# server sends back:
class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    email: str


# /login returns:
class Token(BaseModel):
    access_token: str
    token_type: str
