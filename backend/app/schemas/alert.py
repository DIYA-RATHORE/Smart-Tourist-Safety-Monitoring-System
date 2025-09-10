# Filename: app/schemas/alert.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.alert import AlertStatus

class EmergencyAlertBase(BaseModel):
    """Base schema for an emergency alert."""
    message: Optional[str] = None

class EmergencyAlertCreate(BaseModel):
    """Schema for a tourist to raise a new alert."""
    latitude: float
    longitude: float
    message: Optional[str] = None

class EmergencyAlertAcknowledge(BaseModel):
    """Schema for a police officer to acknowledge an alert."""
    pass

class EmergencyAlertClose(BaseModel):
    """Schema for a police officer to close an alert."""
    pass

class EmergencyAlertResponse(EmergencyAlertBase):
    """Schema for a detailed emergency alert response."""
    id: int
    tourist_id: int
    location: dict  # GeoJSON representation
    timestamp: datetime
    status: AlertStatus
    acknowledged_by: Optional[int] = None

class EmergencyAlertHistory(EmergencyAlertResponse):
    """Schema for fetching alert history."""
    pass
