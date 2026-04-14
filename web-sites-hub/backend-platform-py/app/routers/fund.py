"""Fund router."""

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

from app.core.response import ok
from app.services import fund_service

router = APIRouter(prefix="/fund", tags=["fund"])


@router.get("/list")
def list_funds() -> dict:
    """List funds."""
    data = fund_service.list_funds()
    return ok(data)


@router.get("/download", response_class=PlainTextResponse)
def download_funds_csv() -> PlainTextResponse:
    """Return CSV for fund records."""
    csv_text = fund_service.export_funds_csv()
    return PlainTextResponse(
        content=csv_text,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=funds.csv"},
    )
