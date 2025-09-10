# Filename: app/schemas/user.py
from pydantic import BaseModel, Field
from app.models.user import UserRole
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    """Base schema for a user."""
    username: str = Field(..., min_length=3, max_length=50)

class UserCreate(UserBase):
    """Schema for creating a new user account."""
    password: str = Field(..., min_length=8)
    role: UserRole = UserRole.TOURIST

class UserInDB(UserBase):
    """Schema for a user retrieved from the database."""
    id: int
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

class UserLogin(UserBase):
    """Schema for user login credentials."""
    password: str

class UserProfile(UserInDB):
    """Schema for a user's full profile, including sensitive info."""
    pass
