"""In-memory sliding-window rate limiting helpers."""

from __future__ import annotations

from collections import defaultdict, deque
import time

from fastapi import Request
from fastapi.responses import JSONResponse

# bucket_key -> request timestamps (seconds)
_BUCKETS: dict[str, deque[float]] = defaultdict(deque)


def get_client_ip(request: Request) -> str:
    """Resolve client IP behind reverse proxies when headers are present."""
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    real_ip = request.headers.get("x-real-ip")
    if real_ip:
        return real_ip.strip()
    if request.client:
        return request.client.host
    return "unknown"


def too_many_requests_response(max_requests: int, window_seconds: int) -> JSONResponse:
    """Build unified 429 JSON response."""
    return JSONResponse(
        status_code=429,
        content={
            "success": False,
            "code": "TOO_MANY_REQUESTS",
            "message": (
                f"Too many requests; limit={max_requests}/{window_seconds}s"
            ),
            "data": None,
        },
    )


def is_rate_limited(bucket_key: str, max_requests: int, window_seconds: int) -> bool:
    """Return True when the bucket is over quota (and record the attempt otherwise)."""
    now = time.time()
    window_start = now - window_seconds
    bucket = _BUCKETS[bucket_key]

    while bucket and bucket[0] < window_start:
        bucket.popleft()

    if len(bucket) >= max_requests:
        return True

    bucket.append(now)
    return False
