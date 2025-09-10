# Filename: app/services/tourist.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
from geoalchemy2.functions import ST_GeomFromText, ST_Contains
import geojson
from app.models.user import User, UserRole
from app.models.tourist import Tourist, GeoFence
from app.schemas.tourist import TouristCreate, TouristUpdate, TouristLocationUpdate
from fastapi import HTTPException, status
from typing import List


async def create_tourist_profile(db: AsyncSession, user_id: int, tourist_in: TouristCreate) -> Tourist:
    """Creates a new tourist profile linked to a user account."""
    db_tourist = Tourist(
        user_id=user_id,
        full_name=tourist_in.full_name,
        passport_id=tourist_in.passport_id,
        contact_number=tourist_in.contact_number
    )
    db.add(db_tourist)
    await db.commit()
    await db.refresh(db_tourist)
    return db_tourist


async def get_tourist_by_user_id(db: AsyncSession, user_id: int) -> Tourist | None:
    """Fetches a tourist profile by their user ID."""
    result = await db.execute(
        select(Tourist)
        .filter(Tourist.user_id == user_id)
        .options(selectinload(Tourist.user))
    )
    return result.scalars().first()


async def get_tourist_by_id(db: AsyncSession, tourist_id: int) -> Tourist | None:
    """Fetches a tourist profile by their tourist ID."""
    result = await db.execute(
        select(Tourist)
        .filter(Tourist.id == tourist_id)
        .options(selectinload(Tourist.user))
    )
    return result.scalars().first()


async def update_tourist_profile(db: AsyncSession, tourist: Tourist, tourist_in: TouristUpdate) -> Tourist:
    """Updates an existing tourist profile."""
    if tourist_in.full_name:
        tourist.full_name = tourist_in.full_name
    if tourist_in.contact_number:
        tourist.contact_number = tourist_in.contact_number

    await db.commit()
    await db.refresh(tourist)
    return tourist


async def update_tourist_location(db: AsyncSession, tourist_id: int, location_in: TouristLocationUpdate) -> Tourist:
    """Updates a tourist's location and checks for geo-fence violations."""
    tourist = await get_tourist_by_id(db, tourist_id)
    if not tourist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tourist not found.")

    point = f'POINT({location_in.longitude} {location_in.latitude})'
    tourist.last_location = ST_GeomFromText(point, 4326)

    # Geo-fence check: Check if the tourist's new location is outside of any geo-fences
    geo_fences = await db.execute(select(GeoFence))
    for fence in geo_fences.scalars():
        is_inside = await db.execute(
            select(ST_Contains(fence.area, tourist.last_location))
        )
        if not is_inside.scalar_one():
            # Trigger alert for geo-fence violation
            # This is where you would call an alert service function
            print(f"ALERT: Tourist {tourist_id} exited geo-fence: {fence.name}")

    await db.commit()
    await db.refresh(tourist)
    return tourist


async def get_all_tourists(db: AsyncSession) -> List[Tourist]:
    """Fetches all tourist profiles from the database."""
    result = await db.execute(
        select(Tourist).options(selectinload(Tourist.user))
    )
    return result.scalars().all()
