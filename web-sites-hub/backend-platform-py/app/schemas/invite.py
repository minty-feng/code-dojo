"""Invite key request/response schemas."""

from datetime import datetime

from pydantic import BaseModel


class VerifyKeyRequest(BaseModel):
    key: str


class GenerateKeyRequest(BaseModel):
    purpose: str = "resume_access"
    expire_days: int | None = None


class InviteKeyOut(BaseModel):
    id: int
    key: str
    purpose: str
    created_at: datetime
    expires_at: datetime
    used: bool
    used_at: datetime | None
    visitor_ip: str | None

    model_config = {"from_attributes": True}
