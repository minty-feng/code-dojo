"""Schemas for auth APIs."""

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    """Login payload."""

    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)


class RefreshRequest(BaseModel):
    """Refresh token payload."""

    refresh_token: str = Field(..., min_length=1)
