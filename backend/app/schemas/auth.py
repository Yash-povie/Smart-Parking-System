"""
Authentication schemas
"""

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    phone_number: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    phone_number: Optional[str]
    role: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class Token(BaseModel):
    access_token: str
    token_type: str


