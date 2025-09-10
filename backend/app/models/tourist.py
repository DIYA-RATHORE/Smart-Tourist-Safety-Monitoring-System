# Filename: app/models/tourist.py
from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from app.models.base import BaseMixin, Base
from sqlalchemy.sql import func

class Tourist(BaseMixin, Base):
    """
    Database model for tourist profiles with KYC information.
    """
    user_id = Column(Integer, ForeignKey('users.id'), unique=True, nullable=False)
    full_name = Column(String, nullable=False)
    passport_id = Column(String, unique=True, nullable=False)
    contact_number = Column(String, nullable=False)
    # PostGIS geometry column for location tracking
    last_location = Column(Geometry(geometry_type='POINT', srid=4326), nullable=True)

    user = relationship("User", backref="tourist", uselist=False)

class GeoFence(BaseMixin, Base):
    """
    Database model for defining safe zones and geo-fences.
    """
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    # PostGIS geometry column for the geo-fence polygon
    area = Column(Geometry(geometry_type='POLYGON', srid=4326), nullable=False)
