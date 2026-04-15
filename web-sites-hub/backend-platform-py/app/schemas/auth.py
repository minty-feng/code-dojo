"""Schemas for auth APIs."""

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    """Login payload."""

    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)


class RefreshRequest(BaseModel):
    """Refresh token payload."""

    refresh_token: str = Field(..., min_length=1)


class RegisterRequest(BaseModel):
    """User register payload."""

    username: str = Field(..., min_length=3, max_length=64)
    password: str = Field(..., min_length=6, max_length=128)
    nickname: str = Field(default="", max_length=64)
    avatar: str = Field(default="🐼", max_length=64)
