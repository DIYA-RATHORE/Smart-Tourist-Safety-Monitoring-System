# Filename: app/models/user.py
import enum
from sqlalchemy import Column, String, Enum, Boolean, DateTime
from app.models.base import BaseMixin, Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class UserRole(str, enum.Enum):
    """Defines the possible user roles."""
    ADMIN = "admin"
    POLICE = "police"
    TOURIST = "tourist"
    CYBERSECURITY = "cybersecurity"


class User(BaseMixin, Base):
    """
    Database model for a user account.
    """
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.TOURIST, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship to EmergencyAlert
    acknowledged_alerts = relationship("EmergencyAlert", back_populates="acknowledged_by_user",
                                       foreign_keys="EmergencyAlert.acknowledged_by")
