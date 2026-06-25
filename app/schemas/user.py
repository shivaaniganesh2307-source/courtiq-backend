from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    skill_level: Optional[str] = "intermediate"
    dominant_hand: Optional[str] = "right"
    play_style: Optional[str] = "baseline"

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    skill_level: Optional[str] = None
    dominant_hand: Optional[str] = None
    play_style: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    skill_level: str
    dominant_hand: str
    play_style: str
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
