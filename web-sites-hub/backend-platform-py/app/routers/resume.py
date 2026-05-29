"""Resume router.

Serves the access-controlled resume page with session-based authentication.
Ported from backend-resume (Rust/Actix-web).

Flow:
  GET  /resume                     — show auth.html or resume.html depending on session
  POST /api/v1/resume/auth         — verify invite key, set session
  POST /api/v1/resume/logout       — clear session
  GET  /api/v1/resume/status       — query session state
"""

from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse

from app.core.database import SessionLocal
from app.core.response import ok
from app.schemas.invite import VerifyKeyRequest
from app.services import invite_service

# Page router — mounted WITHOUT /api/v1 prefix
page_router = APIRouter(tags=["resume"])

# API router — mounted WITH /api/v1 prefix
api_router = APIRouter(prefix="/resume", tags=["resume"])

_TMPL_DIR = Path(__file__).resolve().parent.parent / "templates" / "resume"
_AUTH_HTML = _TMPL_DIR / "auth.html"
_RESUME_HTML = _TMPL_DIR / "resume.html"

_SESSION_KEY = "resume_authenticated"


def _is_authenticated(request: Request) -> bool:
    return bool(request.session.get(_SESSION_KEY))


# ── Page route ────────────────────────────────────────────────────────────────

@page_router.get("/resume", response_class=HTMLResponse, include_in_schema=False)
def resume_page(request: Request) -> HTMLResponse:
    """Serve auth page or resume page depending on session state."""
    if _is_authenticated(request):
        content = _RESUME_HTML.read_text(encoding="utf-8")
    else:
        content = _AUTH_HTML.read_text(encoding="utf-8")
    return HTMLResponse(
        content=content,
        headers={
            "Cache-Control": "no-store, no-cache, must-revalidate",
            "Pragma": "no-cache",
        },
    )


# ── API routes ────────────────────────────────────────────────────────────────

@api_router.post("/auth")
def resume_auth(payload: VerifyKeyRequest, request: Request) -> JSONResponse:
    """Verify invite key and establish session.

    On success the key is consumed and session is set; pool is replenished.
    """
    client_ip = request.client.host if request.client else ""
    with SessionLocal() as db:
        invite_service.verify_key(db, payload.key, visitor_ip=client_ip)
    request.session[_SESSION_KEY] = True
    return JSONResponse(content=ok(None, "验证成功"))


@api_router.post("/logout")
def resume_logout(request: Request) -> JSONResponse:
    """Clear resume session."""
    request.session.pop(_SESSION_KEY, None)
    return JSONResponse(
        content=ok(None, "已退出"),
        headers={"Cache-Control": "no-store"},
    )


@api_router.get("/status")
def resume_status(request: Request) -> dict:
    """Return current session authentication state."""
    return ok({"authenticated": _is_authenticated(request)})
