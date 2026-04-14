"""Unified response helpers.

All routers should return this shape so frontend integration stays stable.
"""

from typing import Any


def ok(data: Any = None, message: str = "ok") -> dict:
    """Return a successful API response payload."""
    return {
        "success": True,
        "code": "OK",
        "message": message,
        "data": data,
    }


def fail(code: str, message: str, data: Any = None) -> dict:
    """Return a failed API response payload."""
    return {
        "success": False,
        "code": code,
        "message": message,
        "data": data,
    }
