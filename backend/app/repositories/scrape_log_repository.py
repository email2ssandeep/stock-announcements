from sqlalchemy.orm import Session
from app.models.scrape_log import ScrapeLog
from app.repositories.base import BaseRepository


class ScrapeLogRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(ScrapeLog, db)

    def get_latest(self) -> ScrapeLog | None:
        return (
            self.db.query(ScrapeLog)
            .order_by(ScrapeLog.scraped_at.desc())
            .first()
        )
