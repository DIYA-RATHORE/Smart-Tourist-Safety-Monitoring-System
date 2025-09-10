# Filename: app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from app.schemas.user import UserCreate, UserLogin, UserInDB
from app.schemas.token import Token
from app.services.user import create_user, get_user_by_username
from app.services.auth import verify_password, create_access_token, get_current_active_user
from app.core.config import settings
from app.database import get_db
from app.services.log import create_access_log, create_failed_login_log
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserInDB)
async def register_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Registers a new user account with a default 'tourist' role.
    **Example Request:**
    ```json
    {
      "username": "john.doe",
      "password": "password123",
      "role": "tourist"
    }
    ```
    **Example Response:**
    ```json
    {
      "username": "john.doe",
      "id": 1,
      "role": "tourist",
      "is_active": true,
      "created_at": "2023-10-27T10:00:00.123Z",
      "updated_at": null
    }
    ```
    """
    db_user = await get_user_by_username(db, username=user_in.username)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")

    new_user = await create_user(db=db, user_in=user_in)
    await create_access_log(db, None, "/auth/register", "POST", True, new_user.role)
    return new_user


@router.post("/login", response_model=Token)
async def login_for_access_token(user_in: UserLogin, db: AsyncSession = Depends(get_db)):
    """
    Logs in a user and returns a JWT access token.
    **Example Request:**
    ```json
    {
      "username": "john.doe",
      "password": "password123"
    }
    ```
    **Example Response:**
    ```json
    {
      "access_token": "eyJhbGciOiJIUzI1Ni...",
      "token_type": "bearer",
      "issued_at": "2023-10-27T10:00:00.123Z",
      "expires_at": "2023-10-27T10:30:00.123Z"
    }
    ```
    """
    db_user = await get_user_by_username(db, username=user_in.username)
    if not db_user or not verify_password(user_in.password, db_user.hashed_password):
        await create_failed_login_log(db, user_in.username, None)
        await create_access_log(db, None, "/auth/login", "POST", False, "unauthenticated")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.username, "role": db_user.role},
        expires_delta=access_token_expires
    )

    await create_access_log(db, db_user.id, "/auth/login", "POST", True, db_user.role)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "issued_at": db_user.created_at,
        "expires_at": db_user.created_at + access_token_expires
    }
