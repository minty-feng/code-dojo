"""Auth router."""

from fastapi import APIRouter

from app.core.response import ok
from app.schemas.auth import LoginRequest, RefreshRequest, RegisterRequest
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login(payload: LoginRequest) -> dict:
    """Authenticate user and return token pair."""
    tokens = auth_service.login(payload.username, payload.password)
    return ok(tokens, "login success")


@router.post("/refresh")
def refresh(payload: RefreshRequest) -> dict:
    """Refresh access token."""
    token = auth_service.refresh_token(payload.refresh_token)
    return ok(token, "refresh success")


@router.post("/register")
def register(payload: RegisterRequest) -> dict:
    """Register new user and return token pair."""
    tokens = auth_service.register(
        username=payload.username,
        password=payload.password,
        nickname=payload.nickname,
        avatar=payload.avatar,
    )
    return ok(tokens, "register success")
