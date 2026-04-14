"""SQLAdmin authentication backend.

This module adds a simple username/password guard for /admin.
"""

from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from app.core.config import settings


class AdminAuthBackend(AuthenticationBackend):
    """Minimal session-based auth backend for SQLAdmin."""

    def __init__(self) -> None:
        super().__init__(secret_key=settings.admin_session_secret)

    async def login(self, request: Request) -> bool:
        """Validate admin credentials from SQLAdmin login form."""
        form = await request.form()
        username = str(form.get("username", ""))
        password = str(form.get("password", ""))

        if username == settings.admin_username and password == settings.admin_password:
            request.session.update({"admin_logged_in": "1"})
            return True
        return False

    async def logout(self, request: Request) -> bool:
        """Clear admin session."""
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        """Allow access only when admin session is present."""
        return request.session.get("admin_logged_in") == "1"
