"""FastAPI application entrypoint.

This file wires routers, exception handlers, and global app config.
"""

import time
import sys
from collections import defaultdict, deque

from fastapi import FastAPI
from fastapi.responses import JSONResponse
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
from app.routers import auth, content, diary, fund, market, poems, system, users

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

# In-memory admin rate limit buckets.
# Key: client host, Value: deque of request timestamps (seconds)
ADMIN_RATE_BUCKETS: dict[str, deque[float]] = defaultdict(deque)

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


@app.middleware("http")
async def admin_localhost_only(request, call_next):
    """Protect /admin with optional localhost-only policy.

    By default, admin is localhost-only.
    Set ADMIN_ALLOW_REMOTE=true to allow remote access through Nginx.
    """
    if request.url.path.startswith("/admin"):
        client_host = request.client.host if request.client else ""
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
        now = time.time()
        window_start = now - settings.admin_rate_limit_window_seconds
        bucket = ADMIN_RATE_BUCKETS[client_host]

        # Drop expired timestamps out of the rate-limit window.
        while bucket and bucket[0] < window_start:
            bucket.popleft()

        # Enforce request quota for /admin.
        if len(bucket) >= settings.admin_rate_limit_max_requests:
            return JSONResponse(
                status_code=429,
                content={
                    "success": False,
                    "code": "TOO_MANY_REQUESTS",
                    "message": (
                        "Too many admin requests; "
                        f"limit={settings.admin_rate_limit_max_requests}/"
                        f"{settings.admin_rate_limit_window_seconds}s"
                    ),
                    "data": None,
                },
            )
        bucket.append(now)
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
app.include_router(diary.router, prefix=settings.api_prefix)
app.include_router(poems.router, prefix=settings.api_prefix)
app.include_router(system.router, prefix=settings.api_prefix)


@app.on_event("startup")
def startup_init_db() -> None:
    """Initialize database schema and seed data at startup."""
    init_db()
