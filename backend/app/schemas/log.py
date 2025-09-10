# Filename: app/schemas/log.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AccessLogResponse(BaseModel):
    """Schema for a single access log entry."""
    id: int
    user_id: Optional[int] = None
    endpoint: str
    method: str
    timestamp: datetime
    is_successful: bool
    role: str

class FailedLoginResponse(BaseModel):
    """Schema for a failed login attempt entry."""
    id: int
    username: str
    ip_address: Optional[str] = None
    timestamp: datetime
