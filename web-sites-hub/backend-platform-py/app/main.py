"""FastAPI application entrypoint.

This file wires routers, exception handlers, and global app config.
"""

import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.core.admin import setup_admin
from app.core.config import settings
from app.core.database import init_db
from app.core.exceptions import (
    AppException,
    app_exception_handler,
    unhandled_exception_handler,
)
from app.core.rate_limit import get_client_ip, is_rate_limited, too_many_requests_response
from app.routers import auth, content, fund, invite, market, poems, snippets, system, users
from app.routers.resume import api_router as resume_api_router, page_router as resume_page_router

REQUIRED_PYTHON_MAJOR = 3
REQUIRED_PYTHON_MINOR = 12

if sys.version_info[:2] != (REQUIRED_PYTHON_MAJOR, REQUIRED_PYTHON_MINOR):
    raise RuntimeError(
        "backend-platform-py requires Python "
        f"{REQUIRED_PYTHON_MAJOR}.{REQUIRED_PYTHON_MINOR}, "
        f"but current is {sys.version_info.major}.{sys.version_info.minor}"
    )

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Single-service backend blueprint for multi-frontend projects.",
)

_API_AUTH_PATHS = frozenset(
    {
        f"{settings.api_prefix}/auth/login",
        f"{settings.api_prefix}/auth/register",
    }
)
_API_INVITE_VERIFY_PATHS = frozenset(
    {
        f"{settings.api_prefix}/invite/verify",
        f"{settings.api_prefix}/resume/auth",
    }
)
_API_INVITE_GENERATE_PATH = f"{settings.api_prefix}/invite/generate"

# Session middleware is required for SQLAdmin login state.
app.add_middleware(SessionMiddleware, secret_key=settings.admin_session_secret)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount SQLAdmin dashboard at /admin.
setup_admin(app)

# Mount resume static assets.
_RESUME_STATIC_DIR = Path(__file__).resolve().parent / "static" / "resume"
app.mount("/static/resume", StaticFiles(directory=_RESUME_STATIC_DIR), name="resume_static")


def _is_catalog_read_path(path: str) -> bool:
    """Return True for public poem/snippet GET routes that should be rate-limited."""
    prefix = settings.api_prefix
    return path.startswith(f"{prefix}/snippets") or path.startswith(f"{prefix}/poems")


@app.middleware("http")
async def api_rate_limit_middleware(request, call_next):
    """Rate-limit sensitive POST routes and public catalog GET routes by client IP."""
    if not settings.rate_limit_enabled:
        return await call_next(request)

    path = request.url.path
    client_ip = get_client_ip(request)

    if request.method == "POST":
        if path in _API_AUTH_PATHS:
            bucket_key = f"auth:{client_ip}"
            if is_rate_limited(
                bucket_key,
                settings.auth_rate_limit_max_requests,
                settings.auth_rate_limit_window_seconds,
            ):
                return too_many_requests_response(
                    settings.auth_rate_limit_max_requests,
                    settings.auth_rate_limit_window_seconds,
                )
        elif path in _API_INVITE_VERIFY_PATHS:
            bucket_key = f"invite_verify:{client_ip}"
            if is_rate_limited(
                bucket_key,
                settings.invite_verify_rate_limit_max_requests,
                settings.invite_verify_rate_limit_window_seconds,
            ):
                return too_many_requests_response(
                    settings.invite_verify_rate_limit_max_requests,
                    settings.invite_verify_rate_limit_window_seconds,
                )
        elif path == _API_INVITE_GENERATE_PATH:
            bucket_key = f"invite_generate:{client_ip}"
            if is_rate_limited(
                bucket_key,
                settings.invite_verify_rate_limit_max_requests,
                settings.invite_verify_rate_limit_window_seconds,
            ):
                return too_many_requests_response(
                    settings.invite_verify_rate_limit_max_requests,
                    settings.invite_verify_rate_limit_window_seconds,
                )
    elif request.method == "GET" and _is_catalog_read_path(path):
        bucket_key = f"catalog:{client_ip}"
        if is_rate_limited(
            bucket_key,
            settings.catalog_rate_limit_max_requests,
            settings.catalog_rate_limit_window_seconds,
        ):
            return too_many_requests_response(
                settings.catalog_rate_limit_max_requests,
                settings.catalog_rate_limit_window_seconds,
            )

    return await call_next(request)


@app.middleware("http")
async def admin_localhost_only(request, call_next):
    """Protect /admin with optional localhost-only policy.

    By default, admin is localhost-only.
    Set ADMIN_ALLOW_REMOTE=true to allow remote access through Nginx.
    """
    if request.url.path.startswith("/admin"):
        client_host = get_client_ip(request)
        if (not settings.admin_allow_remote) and client_host not in {"127.0.0.1", "::1", "localhost"}:
            return JSONResponse(
                status_code=403,
                content={
                    "success": False,
                    "code": "FORBIDDEN",
                    "message": "Admin panel is restricted to localhost only (set ADMIN_ALLOW_REMOTE=true to allow remote access)",
                    "data": None,
                },
            )
        bucket_key = f"admin:{client_host}"
        if is_rate_limited(
            bucket_key,
            settings.admin_rate_limit_max_requests,
            settings.admin_rate_limit_window_seconds,
        ):
            return too_many_requests_response(
                settings.admin_rate_limit_max_requests,
                settings.admin_rate_limit_window_seconds,
            )
    return await call_next(request)

# Register custom exception handlers.
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

# Register routers under one API prefix.
app.include_router(auth.router, prefix=settings.api_prefix)
app.include_router(users.router, prefix=settings.api_prefix)
app.include_router(content.router, prefix=settings.api_prefix)
app.include_router(fund.router, prefix=settings.api_prefix)
app.include_router(market.router, prefix=settings.api_prefix)
app.include_router(poems.router, prefix=settings.api_prefix)
app.include_router(snippets.router, prefix=settings.api_prefix)
app.include_router(invite.router, prefix=settings.api_prefix)
app.include_router(system.router, prefix=settings.api_prefix)
# Resume: page route at /resume (no prefix), API sub-routes under /api/v1/resume.
app.include_router(resume_page_router)
app.include_router(resume_api_router, prefix=settings.api_prefix)


@app.on_event("startup")
def startup_init_db() -> None:
    """Initialize database schema and seed data at startup."""
    init_db()
