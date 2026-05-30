"""Custom exception definitions and handlers."""

import logging

from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.response import fail

logger = logging.getLogger(__name__)


class AppException(Exception):
    """Business exception with explicit HTTP status and error code."""

    def __init__(self, status_code: int, code: str, message: str):
        self.status_code = status_code
        self.code = code
        self.message = message
        super().__init__(message)


async def app_exception_handler(_: Request, exc: AppException) -> JSONResponse:
    """Convert AppException to unified JSON response."""
    return JSONResponse(
        status_code=exc.status_code,
        content=fail(code=exc.code, message=exc.message),
    )


async def unhandled_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    """Catch unexpected errors and hide internal details from clients."""
    logger.exception("Unhandled API error: %s", exc)
    return JSONResponse(
        status_code=500,
        content=fail(code="INTERNAL_ERROR", message="Internal server error"),
    )
