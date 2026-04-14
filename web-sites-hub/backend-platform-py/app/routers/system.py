"""System router."""

from fastapi import APIRouter

from app.core.config import settings
from app.core.response import ok

router = APIRouter(prefix="/system", tags=["system"])


@router.get("/health")
def health() -> dict:
    """Simple health endpoint for probes."""
    return ok({"status": "healthy"})


@router.get("/info")
def info() -> dict:
    """Service info endpoint."""
    return ok(
        {
            "name": settings.app_name,
            "version": settings.app_version,
            "api_prefix": settings.api_prefix,
        }
    )
