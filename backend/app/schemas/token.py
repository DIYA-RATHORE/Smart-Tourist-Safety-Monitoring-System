# Filename: app/schemas/token.py
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class Token(BaseModel):
    """Schema for a JWT access token response."""
    access_token: str
    token_type: str
    issued_at: datetime
    expires_at: datetime

class TokenData(BaseModel):
    """Schema for the payload contained within a JWT."""
    username: str | None = None
    role: str | None = None

    model_config = ConfigDict(from_attributes=True)
