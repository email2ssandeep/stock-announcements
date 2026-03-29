import logging
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.announcement import Announcement
from app.repositories.announcement_repository import AnnouncementRepository
from app.repositories.company_repository import CompanyRepository
from app.repositories.scrape_log_repository import ScrapeLogRepository
from app.models.scrape_log import ScrapeLog
from app.services import cache_service, scraper_service

logger = logging.getLogger(__name__)
CACHE_KEY = "all_announcements"


def _build_response(db: Session) -> dict:
    company_repo = CompanyRepository(db)
    ann_repo = AnnouncementRepository(db)
    result = {}
    for company in company_repo.get_all():
        announcements = ann_repo.get_by_company(company.id)
        result[company.ticker] = [
            {"date": a.announcement_date, "title": a.title, "source_url": a.source_url}
            for a in announcements
        ]
    return result


def get_all_announcements(db: Session) -> dict:
    cached = cache_service.get(CACHE_KEY)
    if cached is not None:
        return cached

    data = _build_response(db)
    cache_service.set(CACHE_KEY, data)
    return data


def get_announcements_for_company(ticker: str, db: Session) -> list[dict]:
    all_data = get_all_announcements(db)
    return all_data.get(ticker, [])


def refresh_announcements(db: Session) -> dict:
    start = datetime.utcnow()
    errors = []
    company_repo = CompanyRepository(db)
    ann_repo = AnnouncementRepository(db)

    scraped = scraper_service.scrape_all()

    for ticker, items in scraped.items():
        company = company_repo.get_by_ticker(ticker)
        if not company:
            logger.warning("Company not found in DB: %s", ticker)
            continue
        if not items:
            errors.append(ticker)
            continue

        new_anns = [
            Announcement(
                company_id=company.id,
                title=item["title"],
                announcement_date=item["date"],
                source_url=item.get("source_url"),
                scraped_at=datetime.utcnow(),
                rank=idx + 1,
            )
            for idx, item in enumerate(items)
        ]
        ann_repo.replace_for_company(company.id, new_anns)

    duration_ms = int((datetime.utcnow() - start).total_seconds() * 1000)
    import json
    log = ScrapeLog(
        scraped_at=datetime.utcnow(),
        companies_fetched=len(scraped) - len(errors),
        errors=json.dumps(errors) if errors else None,
        duration_ms=duration_ms,
    )
    ScrapeLogRepository(db).add(log)

    cache_service.invalidate(CACHE_KEY)
    data = _build_response(db)
    cache_service.set(CACHE_KEY, data)

    logger.info("Refresh complete: %d companies, %d errors, %dms", len(scraped), len(errors), duration_ms)
    return data
