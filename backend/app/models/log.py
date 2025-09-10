# Filename: app/models/log.py
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Boolean
from app.models.base import BaseMixin, Base
from sqlalchemy.sql import func

class AccessLog(BaseMixin, Base):
    """
    Database model for logging every API access.
    """
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    endpoint = Column(String, nullable=False)
    method = Column(String(length=10), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    is_successful = Column(Boolean, nullable=False)
    role = Column(String, nullable=False)

class FailedLoginAttempt(BaseMixin, Base):
    """
    Database model for logging failed login attempts.
    """
    username = Column(String, nullable=False)
    ip_address = Column(String, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
