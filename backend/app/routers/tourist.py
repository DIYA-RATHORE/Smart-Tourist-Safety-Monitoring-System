# Filename: app/routers/tourist.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.tourist import TouristCreate, TouristUpdate, TouristLocationUpdate, TouristProfile
from app.schemas.user import UserInDB
from app.services import tourist as tourist_service
from app.services.auth import get_current_active_user, get_current_active_police_or_admin
from app.services.log import create_access_log
from app.database import get_db
from app.models.user import User

router = APIRouter(prefix="/tourists", tags=["Tourist Management"])


@router.post("/", response_model=TouristProfile)
async def create_tourist(
        tourist_in: TouristCreate,
        current_user: User = Depends(get_current_active_user),
        db: AsyncSession = Depends(get_db)
):
    """
    Creates a new tourist profile for the authenticated user.
    **Example Request:**
    ```json
    {
      "full_name": "Jane Smith",
      "passport_id": "P12345678",
      "contact_number": "+1234567890"
    }
    ```
    **Example Response:**
    ```json
    {
      "id": 1,
      "full_name": "Jane Smith",
      "passport_id": "P12345678",
      "contact_number": "+1234567890",
      "user": {
        "id": 1,
        "username": "janesmith",
        "role": "tourist",
        "is_active": true,
        "created_at": "2023-10-27T10:00:00.123Z",
        "updated_at": null
      }
    }
    ```
    """
    existing_profile = await tourist_service.get_tourist_by_user_id(db, current_user.id)
    if existing_profile:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Tourist profile already exists for this user.")

    new_tourist = await tourist_service.create_tourist_profile(db, current_user.id, tourist_in)
    await create_access_log(db, current_user.id, "/tourists/", "POST", True, current_user.role)
    return new_tourist


@router.get("/me", response_model=TouristProfile)
async def read_tourist_me(
        current_user: User = Depends(get_current_active_user),
        db: AsyncSession = Depends(get_db)
):
    """
    Retrieves the tourist profile of the authenticated user.
    **Example Response:**
    ```json
    {
      "id": 1,
      "full_name": "Jane Smith",
      "passport_id": "P12345678",
      "contact_number": "+1234567890",
      "user": {
        "id": 1,
        "username": "janesmith",
        "role": "tourist",
        "is_active": true,
        "created_at": "2023-10-27T10:00:00.123Z",
        "updated_at": null
      }
    }
    ```
    """
    tourist_profile = await tourist_service.get_tourist_by_user_id(db, current_user.id)
    if not tourist_profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Tourist profile not found. Please create one.")

    await create_access_log(db, current_user.id, "/tourists/me", "GET", True, current_user.role)
    return tourist_profile


@router.put("/me", response_model=TouristProfile)
async def update_tourist_me(
        tourist_in: TouristUpdate,
        current_user: User = Depends(get_current_active_user),
        db: AsyncSession = Depends(get_db)
):
    """
    Updates the tourist profile of the authenticated user.
    **Example Request:**
    ```json
    {
      "contact_number": "+0987654321"
    }
    ```
    **Example Response:**
    ```json
    {
      "id": 1,
      "full_name": "Jane Smith",
      "passport_id": "P12345678",
      "contact_number": "+0987654321",
      "user": {
        "id": 1,
        "username": "janesmith",
        "role": "tourist",
        "is_active": true,
        "created_at": "2023-10-27T10:00:00.123Z",
        "updated_at": null
      }
    }
    ```
    """
    tourist_profile = await tourist_service.get_tourist_by_user_id(db, current_user.id)
    if not tourist_profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tourist profile not found.")

    updated_tourist = await tourist_service.update_tourist_profile(db, tourist_profile, tourist_in)
    await create_access_log(db, current_user.id, "/tourists/me", "PUT", True, current_user.role)
    return updated_tourist


@router.put("/me/location", response_model=TouristProfile)
async def update_tourist_location(
        location_in: TouristLocationUpdate,
        current_user: User = Depends(get_current_active_user),
        db: AsyncSession = Depends(get_db)
):
    """
    Updates the current location of the authenticated tourist.
    This endpoint also triggers a geo-fence check.
    **Example Request:**
    ```json
    {
      "latitude": 34.0522,
      "longitude": -118.2437
    }
    ```
    **Example Response:**
    ```json
    {
      "id": 1,
      "full_name": "Jane Smith",
      "passport_id": "P12345678",
      "contact_number": "+1234567890",
      "last_location": {
        "type": "Point",
        "coordinates": [-118.2437, 34.0522]
      },
      "user": { ... }
    }
    ```
    """
    tourist_profile = await tourist_service.get_tourist_by_user_id(db, current_user.id)
    if not tourist_profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tourist profile not found.")

    updated_profile = await tourist_service.update_tourist_location(db, tourist_profile.id, location_in)
    await create_access_log(db, current_user.id, "/tourists/me/location", "PUT", True, current_user.role)
    return updated_profile


@router.get("/", response_model=list[TouristProfile])
async def read_all_tourists(
        current_user: User = Depends(get_current_active_police_or_admin),
        db: AsyncSession = Depends(get_db)
):
    """
    Retrieves a list of all tourist profiles.
    Requires 'police' or 'admin' role.
    **Example Response:**
    ```json
    [
      {
        "id": 1,
        "full_name": "Jane Smith",
        "passport_id": "P12345678",
        "contact_number": "+1234567890",
        "user": { ... }
      },
      {
        "id": 2,
        "full_name": "John Doe",
        "passport_id": "P87654321",
        "contact_number": "+0987654321",
        "user": { ... }
      }
    ]
    ```
    """
    tourists = await tourist_service.get_all_tourists(db)
    await create_access_log(db, current_user.id, "/tourists/", "GET", True, current_user.role)
    return tourists


@router.get("/{tourist_id}", response_model=TouristProfile)
async def read_tourist_by_id(
        tourist_id: int,
        current_user: User = Depends(get_current_active_police_or_admin),
        db: AsyncSession = Depends(get_db)
):
    """
    Retrieves a single tourist profile by ID.
    Requires 'police' or 'admin' role.
    **Example Response:**
    ```json
    {
      "id": 1,
      "full_name": "Jane Smith",
      "passport_id": "P12345678",
      "contact_number": "+1234567890",
      "user": { ... }
    }
    ```
    """
    tourist_profile = await tourist_service.get_tourist_by_id(db, tourist_id)
    if not tourist_profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tourist not found.")

    await create_access_log(db, current_user.id, f"/tourists/{tourist_id}", "GET", True, current_user.role)
    return tourist_profile
