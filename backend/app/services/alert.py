# Filename: app/models/alert.py
import enum
from sqlalchemy import Column, String, DateTime, Enum, Integer, ForeignKey
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from app.models.base import BaseMixin, Base
from sqlalchemy.sql import func

class AlertStatus(str, enum.Enum):
    """Defines the possible statuses for an emergency alert."""
    ACTIVE = "active"
    ACKNOWLEDGED = "acknowledged"
    CLOSED = "closed"

class EmergencyAlert(BaseMixin, Base):
    """
    Database model for emergency alerts raised by tourists.
    """
    tourist_id = Column(Integer, ForeignKey('tourists.id'), nullable=False)
    location = Column(Geometry(geometry_type='POINT', srid=4326), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(Enum(AlertStatus), default=AlertStatus.ACTIVE, nullable=False)
    message = Column(String, nullable=True)
    acknowledged_by = Column(Integer, ForeignKey('users.id'), nullable=True)

    tourist = relationship("Tourist", backref="alerts")
    acknowledged_by_user = relationship("User", back_populates="acknowledged_alerts", foreign_keys=[acknowledged_by])
