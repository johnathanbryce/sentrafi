from pydantic import BaseModel, EmailStr, ConfigDict


# client sends to /auth/register:
class UserCreate(BaseModel):
    email: EmailStr
    password: str


# server sends back:
class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    email: str


# /auth/login returns:
class Token(BaseModel):
    access_token: str
    token_type: str
