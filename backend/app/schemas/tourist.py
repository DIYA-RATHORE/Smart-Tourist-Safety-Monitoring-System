# Filename: app/schemas/tourist.py
from pydantic import BaseModel, Field
from typing import Optional
from app.schemas.user import UserProfile

class TouristBase(BaseModel):
    """Base schema for a tourist profile."""
    full_name: str = Field(..., min_length=3)
    passport_id: str = Field(..., min_length=5)
    contact_number: str = Field(..., min_length=8)

class TouristCreate(TouristBase):
    """Schema for creating a new tourist profile."""
    pass

class TouristUpdate(BaseModel):
    """Schema for updating a tourist profile."""
    full_name: Optional[str] = None
    contact_number: Optional[str] = None

class TouristLocationUpdate(BaseModel):
    """Schema for updating a tourist's location."""
    latitude: float
    longitude: float

class TouristProfile(TouristBase):
    """Schema for a full tourist profile with user info."""
    id: int
    user: UserProfile

class GeoFenceCreate(BaseModel):
    """Schema for creating a geo-fence."""
    name: str = Field(..., min_length=3)
    description: Optional[str] = None
    # GeoJSON representation of a polygon
    geojson: dict = Field(..., description="GeoJSON Polygon object for the geo-fence area.")

class GeoFenceResponse(GeoFenceCreate):
    """Schema for a geo-fence response."""
    id: int
