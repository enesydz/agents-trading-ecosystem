"""Health check endpoints."""

from datetime import UTC, datetime

from fastapi import APIRouter, status

router = APIRouter(prefix="/health")


@router.get("", status_code=status.HTTP_200_OK)
async def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "timestamp": datetime.now(UTC).isoformat(),
    }


@router.get("/ready", status_code=status.HTTP_200_OK)
async def readiness_check() -> dict[str, str]:
    # TODO: verify Redis and PostgreSQL connectivity
    return {"status": "ready"}
