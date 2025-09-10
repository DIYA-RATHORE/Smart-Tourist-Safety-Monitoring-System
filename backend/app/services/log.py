# Filename: app/services/log.py
import csv
import json
import io
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, func
from datetime import datetime
from app.models.log import AccessLog, FailedLoginAttempt
from typing import List


async def create_access_log(db: AsyncSession, user_id: int | None, endpoint: str, method: str, is_successful: bool,
                            role: str):
    """Logs an API access event."""
    stmt = insert(AccessLog).values(
        user_id=user_id,
        endpoint=endpoint,
        method=method,
        is_successful=is_successful,
        role=role
    )
    await db.execute(stmt)
    await db.commit()


async def create_failed_login_log(db: AsyncSession, username: str, ip_address: str | None):
    """Logs a failed login attempt."""
    stmt = insert(FailedLoginAttempt).values(
        username=username,
        ip_address=ip_address
    )
    await db.execute(stmt)
    await db.commit()


async def get_all_access_logs(db: AsyncSession) -> List[AccessLog]:
    """Fetches all API access logs."""
    result = await db.execute(select(AccessLog).order_by(AccessLog.timestamp.desc()))
    return result.scalars().all()


async def get_all_failed_login_logs(db: AsyncSession) -> List[FailedLoginAttempt]:
    """Fetches all failed login attempts."""
    result = await db.execute(select(FailedLoginAttempt).order_by(FailedLoginAttempt.timestamp.desc()))
    return result.scalars().all()


def export_logs_csv(logs: List[dict]) -> str:
    """Converts a list of log dictionaries to a CSV string."""
    if not logs:
        return ""

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=logs[0].keys())
    writer.writeheader()
    writer.writerows(logs)
    return output.getvalue()


def export_logs_json(logs: List[dict]) -> str:
    """Converts a list of log dictionaries to a JSON string."""
    return json.dumps(logs, indent=4, default=str)
