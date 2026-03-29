import json
import logging
from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.health import HealthOut
from app.services import cache_service, announcement_service
from app.repositories.scrape_log_repository import ScrapeLogRepository
from app.config import ADMIN_KEY

router = APIRouter(prefix="/api", tags=["health"])
logger = logging.getLogger(__name__)

CACHE_KEY = "all_announcements"


@router.get("/health", response_model=HealthOut)
def health_check(db: Session = Depends(get_db)):
    log = ScrapeLogRepository(db).get_latest()
    age = cache_service.cache_age_seconds(CACHE_KEY)

    errors = []
    if log and log.errors:
        try:
            errors = json.loads(log.errors)
        except Exception:
            errors = [log.errors]

    return HealthOut(
        status="ok",
        cache_age_seconds=round(age, 1) if age is not None else None,
        last_scraped_at=log.scraped_at.isoformat() if log else None,
        last_scrape_duration_ms=log.duration_ms if log else None,
        last_errors=errors,
    )


@router.post("/refresh")
def manual_refresh(
    x_admin_key: str = Header(default=""),
    db: Session = Depends(get_db),
):
    if x_admin_key != ADMIN_KEY:
        raise HTTPException(status_code=403, detail="Invalid admin key")
    try:
        data = announcement_service.refresh_announcements(db)
        return {"status": "ok", "companies": list(data.keys())}
    except Exception as e:
        logger.exception("Manual refresh failed: %s", e)
        raise HTTPException(status_code=503, detail="Refresh failed")
