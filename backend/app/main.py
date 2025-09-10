# Filename: app/main.py
from fastapi import FastAPI, Depends, Request
from app.core.config import settings
from app.routers import auth, tourist, alert
from app.services.log import create_access_log
from app.services.auth import get_current_user
from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User

app = FastAPI(
    title=settings.APP_NAME,
    description="Backend API for Tourist Safety & Emergency Management System",
    version=settings.API_VERSION
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(tourist.router, prefix="/api/v1")
app.include_router(alert.router, prefix="/api/v1")


@app.middleware("http")
async def log_access(request: Request, call_next):
    """
    Middleware to log every API access.
    """
    user_id = None
    role = "unauthenticated"
    is_successful = True

    try:
        response = await call_next(request)

        # Log successful requests with user info
        db: AsyncSession = request.app.state.db
        user: User | None = await get_current_user(request.headers.get("Authorization", "").replace("Bearer ", ""), db)
        if user:
            user_id = user.id
            role = user.role

        await create_access_log(db, user_id, request.url.path, request.method, is_successful, role)
        return response
    except Exception as e:
        is_successful = False
        await create_access_log(db, user_id, request.url.path, request.method, is_successful, role)
        raise e


@app.on_event("startup")
async def startup_event():
    """Initializes database and other resources on startup."""
    # This is a good place to set up the DB session for middleware
    from app.database import AsyncSessionLocal
    app.state.db = AsyncSessionLocal()


@app.on_event("shutdown")
async def shutdown_event():
    """Closes database connection on shutdown."""
    await app.state.db.close()
