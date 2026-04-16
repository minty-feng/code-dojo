"""Application configuration module.

This file centralizes all runtime configuration. In production you can
replace hardcoded defaults with environment variables.
"""

import os

from pydantic import BaseModel


class Settings(BaseModel):
    """Global runtime settings for the backend service."""

    app_name: str = "backend-platform-py"
    api_prefix: str = "/api/v1"
    app_version: str = "1.0.0"
    jwt_secret: str = os.getenv("JWT_SECRET", "change-this-secret-in-production")
    jwt_algorithm: str = "HS256"
    access_token_exp_minutes: int = 60
    refresh_token_exp_days: int = 14
    admin_username: str = os.getenv("ADMIN_USERNAME", "admin")
    admin_password: str = os.getenv("ADMIN_PASSWORD", "admin123")
    admin_session_secret: str = os.getenv("ADMIN_SESSION_SECRET", "change-admin-session-secret")
    admin_allow_remote: bool = os.getenv("ADMIN_ALLOW_REMOTE", "false").lower() in {
        "1",
        "true",
        "yes",
        "on",
    }
    admin_rate_limit_max_requests: int = int(os.getenv("ADMIN_RATE_LIMIT_MAX_REQUESTS", "30"))
    admin_rate_limit_window_seconds: int = int(os.getenv("ADMIN_RATE_LIMIT_WINDOW_SECONDS", "60"))
    cors_allow_origins: list[str] = [
        origin.strip()
        for origin in os.getenv(
            "CORS_ALLOW_ORIGINS",
            (
                "http://127.0.0.1:5500,http://localhost:5500,"
                "http://127.0.0.1:8000,http://localhost:8000,"
                "http://127.0.0.1:8300,http://localhost:8300"
            ),
        ).split(",")
        if origin.strip()
    ]


settings = Settings()
