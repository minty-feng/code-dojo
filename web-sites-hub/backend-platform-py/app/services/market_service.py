"""Market data helpers (spot quotes, optional upstream providers)."""

from __future__ import annotations

import math
import sqlite3
import time
from datetime import datetime, timedelta, timezone
from collections import deque
from typing import Any

import requests

from app.core.database import DB_PATH
from app.core.config import settings

GOLDAPI_URL = "https://www.goldapi.io/api/XAU/USD"
STOOQ_XAU_DAILY_CSV_URL = "https://stooq.com/q/d/l/?s=xauusd&i=d"
TROY_OZ_GRAMS = 31.1034768
THIRTY_MIN_SECONDS = 30 * 60

_QUOTE_CACHE: dict[str, Any] = {
    "data": None,
    "fetched_at": 0.0,
}
# 14 days x 48 points/day
_INTRADAY_30M: deque[dict[str, Any]] = deque(maxlen=14 * 48)


def _demo_quote(now: float | None = None) -> dict[str, Any]:
    """Deterministic-enough wobble for UI when no vendor token is configured."""
    t = now if now is not None else time.time()
    base = 2680.0
    wobble = 14.0 * math.sin(t / 2200.0) + 6.0 * math.sin(t / 400.0)
    price = round(base + wobble, 2)
    prev = round(base + 14.0 * math.sin((t - 3600.0) / 2200.0) + 6.0 * math.sin((t - 3600.0) / 400.0), 2)
    ch = round(price - prev, 2)
    chp = round((ch / prev) * 100, 3) if prev else 0.0
    return {
        "symbol": "XAUUSD",
        "metal": "XAU",
        "currency": "USD",
        "unit": "troy_oz",
        "price_usd_oz": price,
        "change_abs": ch,
        "change_percent": chp,
        "as_of_ms": int(t * 1000),
        "source": "demo_synthetic",
        "demo": True,
        "upstream_error": False,
        "grams_per_troy_oz": TROY_OZ_GRAMS,
    }


def _bucket_30m_ms(ts_ms: int) -> int:
    sec = ts_ms // 1000
    return (sec - (sec % THIRTY_MIN_SECONDS)) * 1000


def _record_intraday_30m_point(quote: dict[str, Any]) -> None:
    """Store one close point per 30m bucket from latest quote."""
    px = float(quote.get("price_usd_oz") or 0.0)
    if px <= 0:
        return
    ts_ms = int(quote.get("as_of_ms") or int(time.time() * 1000))
    bucket_ms = _bucket_30m_ms(ts_ms)
    if _INTRADAY_30M and _INTRADAY_30M[-1]["bucket_ms"] == bucket_ms:
        _INTRADAY_30M[-1].update({"close_usd_oz": round(px, 2), "as_of_ms": ts_ms})
        return
    _INTRADAY_30M.append(
        {
            "bucket_ms": bucket_ms,
            "as_of_ms": ts_ms,
            "close_usd_oz": round(px, 2),
            "source": quote.get("source", "unknown"),
            "demo": bool(quote.get("demo", True)),
        }
    )


def get_gold_quote_usd() -> dict[str, Any]:
    """Return spot-style gold in USD per troy ounce.

    When ``GOLDAPI_IO_TOKEN`` is set, calls goldapi.io; otherwise returns a
    clearly marked demo payload suitable for UI integration tests.
    """
    token = (settings.goldapi_io_token or "").strip()
    if not token:
        data = _demo_quote()
        _record_intraday_30m_point(data)
        return data

    now = time.time()
    min_interval = max(60, int(settings.goldapi_upstream_min_interval_seconds))
    cached = _QUOTE_CACHE.get("data")
    fetched_at = float(_QUOTE_CACHE.get("fetched_at") or 0.0)
    if cached and (now - fetched_at) < min_interval:
        return cached

    try:
        resp = requests.get(
            GOLDAPI_URL,
            headers={"x-access-token": token},
            timeout=6,
        )
        if resp.status_code != 200:
            data = _demo_quote()
            data["upstream_error"] = True
            data["upstream_status"] = resp.status_code
            data["upstream_body"] = (resp.text or "")[:200]
            _QUOTE_CACHE["data"] = data
            _QUOTE_CACHE["fetched_at"] = now
            _record_intraday_30m_point(data)
            return data
        payload = resp.json()
        price = float(payload.get("price") or 0)
        if price <= 0:
            data = _demo_quote()
            data["upstream_error"] = True
            _QUOTE_CACHE["data"] = data
            _QUOTE_CACHE["fetched_at"] = now
            _record_intraday_30m_point(data)
            return data
        chp = payload.get("chp")
        if chp is None and payload.get("prev_close_price"):
            prev = float(payload["prev_close_price"])
            chp = round((price - prev) / prev * 100, 4) if prev else 0.0
        chp_f = float(chp) if chp is not None else 0.0
        ch = float(payload.get("ch") or (price * chp_f / 100.0))
        ts = payload.get("timestamp")
        if isinstance(ts, (int, float)) and ts > 1e12:
            as_of_ms = int(ts)
        elif isinstance(ts, (int, float)) and ts > 1e9:
            as_of_ms = int(ts * 1000)
        else:
            as_of_ms = int(time.time() * 1000)
        data = {
            "symbol": str(payload.get("symbol") or "XAUUSD"),
            "metal": str(payload.get("metal") or "XAU"),
            "currency": str(payload.get("currency") or "USD"),
            "unit": "troy_oz",
            "price_usd_oz": round(price, 2),
            "change_abs": round(ch, 2),
            "change_percent": round(chp_f, 4),
            "as_of_ms": as_of_ms,
            "source": "goldapi.io",
            "demo": False,
            "upstream_error": False,
            "grams_per_troy_oz": TROY_OZ_GRAMS,
        }
        _QUOTE_CACHE["data"] = data
        _QUOTE_CACHE["fetched_at"] = now
        _record_intraday_30m_point(data)
        return data
    except (requests.RequestException, ValueError, TypeError):
        data = _demo_quote()
        data["upstream_error"] = True
        _QUOTE_CACHE["data"] = data
        _QUOTE_CACHE["fetched_at"] = now
        _record_intraday_30m_point(data)
        return data


def _estimate_from_closes(closes: list[float], latest: float) -> dict[str, Any]:
    """Build a simple next-day estimate using daily close returns."""
    returns: list[float] = []
    for i in range(1, len(closes)):
        prev = closes[i - 1]
        cur = closes[i]
        if prev > 0:
            returns.append((cur / prev) - 1.0)
    if not returns:
        return {
            "mean_daily_return": 0.0,
            "volatility_daily": 0.0,
            "next_day_expected": latest,
            "next_day_range_1sigma": [latest, latest],
        }
    win = returns[-20:] if len(returns) >= 20 else returns
    mean = sum(win) / len(win)
    var = sum((x - mean) ** 2 for x in win) / len(win)
    sigma = math.sqrt(max(var, 0.0))
    exp_px = latest * (1.0 + mean)
    lo = max(0.0, exp_px * (1.0 - sigma))
    hi = exp_px * (1.0 + sigma)
    return {
        "mean_daily_return": round(mean, 6),
        "volatility_daily": round(sigma, 6),
        "next_day_expected": round(exp_px, 2),
        "next_day_range_1sigma": [round(lo, 2), round(hi, 2)],
    }


def _demo_daily_history(days: int) -> dict[str, Any]:
    """Generate synthetic daily close series for UI estimation fallback."""
    now = datetime.now(timezone.utc)
    items: list[dict[str, Any]] = []
    closes: list[float] = []
    for i in range(days):
        ts = now - timedelta(days=(days - 1 - i))
        epoch = ts.timestamp()
        close = 2680.0 + 32.0 * math.sin(epoch / 920000.0) + 12.0 * math.sin(epoch / 240000.0)
        close = round(close, 2)
        items.append({"date": ts.date().isoformat(), "close_usd_oz": close})
        closes.append(close)
    latest = closes[-1] if closes else 0.0
    return {
        "symbol": "XAUUSD",
        "unit": "troy_oz",
        "granularity": "daily",
        "source": "demo_synthetic_daily",
        "demo": True,
        "upstream_error": False,
        "items": items,
        "summary": _estimate_from_closes(closes, latest),
    }


def _days_to_month_points(days: int) -> int:
    """Map a requested day window to an approximate monthly sample count."""
    average_days_per_month = 365.2425 / 12.0
    return max(1, math.ceil(days / average_days_per_month))


def get_gold_daily_history(days: int = 120) -> dict[str, Any]:
    """Return daily close history and a simple next-day estimate.

    Data source priority:
    1) Free stooq CSV daily feed (no key)
    2) Synthetic demo fallback (for stable local/dev behavior)
    """
    days = max(30, min(int(days), 3650))
    # 0) Prefer locally imported workbook data if present.
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute(
            """
            SELECT col_1, usd
            FROM gold_price_since_1978_monthly_avg
            WHERE usd IS NOT NULL AND usd NOT IN ('', '#N/A', 'N/A', 'null', 'NULL')
            ORDER BY col_1 ASC
            """
        )
        rows = cur.fetchall()
        conn.close()
        if rows:
            items: list[dict[str, Any]] = []
            for dt_raw, usd_raw in rows:
                try:
                    d = datetime.fromisoformat(str(dt_raw)).date().isoformat()
                    v = float(usd_raw)
                    if v <= 0:
                        continue
                    items.append({"date": d, "close_usd_oz": round(v, 2)})
                except (ValueError, TypeError):
                    continue
            if items:
                month_points = _days_to_month_points(days)
                items = items[-month_points:]
                closes = [x["close_usd_oz"] for x in items]
                latest = closes[-1]
                return {
                    "symbol": "XAUUSD",
                    "unit": "troy_oz",
                    "granularity": "monthly",
                    "source": "sqlite:gold_price_since_1978_monthly_avg",
                    "demo": False,
                    "upstream_error": False,
                    "items": items,
                    "summary": _estimate_from_closes(closes, latest),
                }
    except sqlite3.Error:
        # Continue to fallback chain below.
        pass

    try:
        resp = requests.get(STOOQ_XAU_DAILY_CSV_URL, timeout=8)
        if resp.status_code != 200:
            demo = _demo_daily_history(days)
            demo["upstream_error"] = True
            demo["upstream_status"] = resp.status_code
            return demo
        text = resp.text or ""
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        if len(lines) <= 1:
            demo = _demo_daily_history(days)
            demo["upstream_error"] = True
            return demo

        raw_items: list[dict[str, Any]] = []
        for ln in lines[1:]:
            parts = ln.split(",")
            if len(parts) < 5:
                continue
            date_s = parts[0].strip()
            close_s = parts[4].strip()
            if close_s in {"", "0", "null", "NULL", "N/A"}:
                continue
            try:
                close_v = float(close_s)
                if close_v <= 0:
                    continue
                raw_items.append({"date": date_s, "close_usd_oz": round(close_v, 2)})
            except ValueError:
                continue
        if not raw_items:
            demo = _demo_daily_history(days)
            demo["upstream_error"] = True
            return demo

        raw_items.sort(key=lambda x: x["date"])
        items = raw_items[-days:]
        closes = [x["close_usd_oz"] for x in items]
        latest = closes[-1]
        return {
            "symbol": "XAUUSD",
            "unit": "troy_oz",
            "granularity": "daily",
            "source": "stooq.com",
            "demo": False,
            "upstream_error": False,
            "items": items,
            "summary": _estimate_from_closes(closes, latest),
        }
    except (requests.RequestException, ValueError, TypeError):
        demo = _demo_daily_history(days)
        demo["upstream_error"] = True
        return demo


def get_gold_intraday_30m(points: int = 96) -> dict[str, Any]:
    """Return rolling 30-minute close points with short-horizon estimate."""
    points = max(24, min(int(points), 14 * 48))
    quote = get_gold_quote_usd()
    _record_intraday_30m_point(quote)
    items = list(_INTRADAY_30M)[-points:]
    closes = [float(x["close_usd_oz"]) for x in items if float(x["close_usd_oz"]) > 0]
    latest = float(quote.get("price_usd_oz") or (closes[-1] if closes else 0.0))
    summary = _estimate_from_closes(closes, latest) if closes else _estimate_from_closes([latest, latest], latest)
    summary_30m = {
        "mean_30m_return": summary["mean_daily_return"],
        "volatility_30m": summary["volatility_daily"],
        "next_30m_expected": summary["next_day_expected"],
        "next_30m_range_1sigma": summary["next_day_range_1sigma"],
    }
    return {
        "symbol": "XAUUSD",
        "unit": "troy_oz",
        "interval": "30m",
        "source": quote.get("source", "unknown"),
        "demo": bool(quote.get("demo", True)),
        "upstream_error": bool(quote.get("upstream_error", False)),
        "items": items,
        "summary": summary_30m,
        "upstream_min_interval_seconds": max(60, int(settings.goldapi_upstream_min_interval_seconds)),
    }
