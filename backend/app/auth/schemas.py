from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, EmailStr, ConfigDict, Field

# --- Auth schemas ---


# client sends to /register:
class UserCreate(BaseModel):
    email: EmailStr
    password: str


# client sends to /login:
class UserLogin(BaseModel):
    email: EmailStr
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


# --- Profile schemas ---


class FinancialGoalCreate(BaseModel):
    name: str = Field(max_length=200)
    target_amount: Optional[Decimal] = None
    priority: int = Field(default=3, ge=1, le=5)
    deadline: Optional[date] = None


class UserProfileCreate(BaseModel):
    profession: Optional[str] = Field(default=None, max_length=100)
    annual_salary: Optional[Decimal] = None
    pay_frequency: Optional[str] = Field(default="biweekly", max_length=20)
    country: Optional[str] = Field(default=None, max_length=3)
    province_or_state: Optional[str] = Field(default=None, max_length=50)
    currency: Optional[str] = Field(default="USD", max_length=3)
    additional_context: Optional[str] = Field(default=None, max_length=500)
    financial_goals: list[FinancialGoalCreate] = Field(
        default_factory=list, max_length=5
    )


class ProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    profession: Optional[str] = None
    annual_salary: Optional[Decimal] = None
    pay_frequency: Optional[str] = None
    country: Optional[str] = None
    province_or_state: Optional[str] = None
    currency: Optional[str] = None
    additional_context: Optional[str] = None


class CreateProfileResponse(BaseModel):
    status: str
    profile: ProfileResponse


class ProfileDetailsResponse(BaseModel):
    profile_details: ProfileResponse
    financial_goals: list[FinancialGoalCreate]


class UserProfileUpdate(BaseModel):
    profession: Optional[str] = Field(default=None, max_length=100)
    annual_salary: Optional[Decimal] = None
    pay_frequency: Optional[str] = Field(default="biweekly", max_length=20)
    country: Optional[str] = Field(default=None, max_length=3)
    province_or_state: Optional[str] = Field(default=None, max_length=50)
    currency: Optional[str] = Field(default="USD", max_length=3)
    additional_context: Optional[str] = Field(default=None, max_length=500)
    financial_goals: Optional[list[FinancialGoalCreate]] = Field(
        default_factory=list, max_length=5
    )
