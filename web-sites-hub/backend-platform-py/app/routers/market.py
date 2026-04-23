"""Public market-style endpoints (spot + daily history helpers)."""

from fastapi import APIRouter
from fastapi.params import Query

from app.core.response import ok
from app.services import market_service

router = APIRouter(prefix="/market", tags=["market"])


@router.get("/gold/quote")
def gold_spot_quote() -> dict:
    """Spot gold quote in USD per troy ounce.

    Configure ``GOLDAPI_IO_TOKEN`` for live vendor data; otherwise a synthetic
    demo series is returned with ``demo: true``.
    """
    return ok(market_service.get_gold_quote_usd())


@router.get("/gold/history")
def gold_daily_history(
    days: int = Query(default=120, ge=30, le=3650),
) -> dict:
    """Daily close history for XAUUSD with next-day estimate summary."""
    return ok(market_service.get_gold_daily_history(days=days))


@router.get("/gold/history-30m")
def gold_intraday_30m(
    points: int = Query(default=96, ge=24, le=672),
) -> dict:
    """Rolling 30m close points with next-30m estimate summary."""
    return ok(market_service.get_gold_intraday_30m(points=points))
