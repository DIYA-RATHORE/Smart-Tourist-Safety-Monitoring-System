# Filename: app/routers/alert.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.alert import EmergencyAlertCreate, EmergencyAlertResponse, EmergencyAlertAcknowledge, \
    EmergencyAlertClose
from app.services import alert as alert_service
from app.services.auth import get_current_active_user, get_current_active_police_or_admin
from app.services.log import create_access_log
from app.database import get_db
from app.models.user import User
from typing import List

router = APIRouter(prefix="/alerts", tags=["Emergency Alerts"])


@router.post("/sos", response_model=EmergencyAlertResponse)
async def create_sos_alert(
        alert_in: EmergencyAlertCreate,
        current_user: User = Depends(get_current_active_user),
        db: AsyncSession = Depends(get_db)
):
    """
    Allows a tourist to raise an emergency SOS alert.
    The user must have a tourist profile.
    **Example Request:**
    ```json
    {
      "latitude": 34.0522,
      "longitude": -118.2437,
      "message": "I need help near the city center!"
    }
    ```
    **Example Response:**
    ```json
    {
      "id": 1,
      "tourist_id": 1,
      "location": {
        "type": "Point",
        "coordinates": [-118.2437, 34.0522]
      },
      "timestamp": "2023-10-27T10:00:00.123Z",
      "status": "active",
      "message": "I need help near the city center!",
      "acknowledged_by": null
    }
    ```
    """
    tourist_profile = await alert_service.get_tourist_by_user_id(db, current_user.id)
    if not tourist_profile:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Tourist profile not found. Cannot raise an alert.")

    new_alert = await alert_service.create_sos_alert(db, tourist_profile.id, alert_in)
    await create_access_log(db, current_user.id, "/alerts/sos", "POST", True, current_user.role)
    return new_alert


@router.get("/active", response_model=List[EmergencyAlertResponse])
async def get_active_alerts(
        current_user: User = Depends(get_current_active_police_or_admin),
        db: AsyncSession = Depends(get_db)
):
    """
    Fetches all currently active emergency alerts.
    Requires 'police' or 'admin' role.
    **Example Response:**
    ```json
    [
      {
        "id": 1,
        "tourist_id": 1,
        "location": { "type": "Point", "coordinates": [-118.2437, 34.0522] },
        "timestamp": "2023-10-27T10:00:00.123Z",
        "status": "active",
        "message": "I need help near the city center!",
        "acknowledged_by": null
      }
    ]
    ```
    """
    alerts = await alert_service.get_all_active_alerts(db)
    await create_access_log(db, current_user.id, "/alerts/active", "GET", True, current_user.role)
    return alerts


@router.put("/{alert_id}/acknowledge", response_model=EmergencyAlertResponse)
async def acknowledge_alert(
        alert_id: int,
        current_user: User = Depends(get_current_active_police_or_admin),
        db: AsyncSession = Depends(get_db)
):
    """
    Allows a police officer or admin to acknowledge an active alert.
    Requires 'police' or 'admin' role.
    **Example Response:**
    ```json
    {
      "id": 1,
      "tourist_id": 1,
      "location": { "type": "Point", "coordinates": [-118.2437, 34.0522] },
      "timestamp": "2023-10-27T10:00:00.123Z",
      "status": "acknowledged",
      "message": "I need help near the city center!",
      "acknowledged_by": 2
    }
    ```
    """
    acknowledged_alert = await alert_service.acknowledge_alert(db, alert_id, current_user.id)
    await create_access_log(db, current_user.id, f"/alerts/{alert_id}/acknowledge", "PUT", True, current_user.role)
    return acknowledged_alert


@router.put("/{alert_id}/close", response_model=EmergencyAlertResponse)
async def close_alert(
        alert_id: int,
        current_user: User = Depends(get_current_active_police_or_admin),
        db: AsyncSession = Depends(get_db)
):
    """
    Allows a police officer or admin to close an acknowledged alert.
    Requires 'police' or 'admin' role.
    **Example Response:**
    ```json
    {
      "id": 1,
      "tourist_id": 1,
      "location": { "type": "Point", "coordinates": [-118.2437, 34.0522] },
      "timestamp": "2023-10-27T10:00:00.123Z",
      "status": "closed",
      "message": "I need help near the city center!",
      "acknowledged_by": 2
    }
    ```
    """
    closed_alert = await alert_service.close_alert(db, alert_id)
    await create_access_log(db, current_user.id, f"/alerts/{alert_id}/close", "PUT", True, current_user.role)
    return closed_alert


@router.get("/history", response_model=List[EmergencyAlertResponse])
async def get_alert_history(
        current_user: User = Depends(get_current_active_police_or_admin),
        db: AsyncSession = Depends(get_db)
):
    """
    Fetches the history of all emergency alerts.
    Requires 'police' or 'admin' role.
    **Example Response:**
    ```json
    [
      {
        "id": 1,
        "tourist_id": 1,
        "location": { "type": "Point", "coordinates": [-118.2437, 34.0522] },
        "timestamp": "2023-10-27T10:00:00.123Z",
        "status": "closed",
        "message": "I need help near the city center!",
        "acknowledged_by": 2
      },
      {
        "id": 2,
        "tourist_id": 2,
        "location": { "type": "Point", "coordinates": [-118.2437, 34.0522] },
        "timestamp": "2023-10-27T10:05:00.123Z",
        "status": "active",
        "message": "I'm lost!",
        "acknowledged_by": null
      }
    ]
    ```
    """
    alerts = await alert_service.get_alert_history(db)
    await create_access_log(db, current_user.id, "/alerts/history", "GET", True, current_user.role)
    return alerts
