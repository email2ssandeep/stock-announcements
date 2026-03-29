from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base


class ScrapeLog(Base):
    __tablename__ = "scrape_log"

    id = Column(Integer, primary_key=True, index=True)
    scraped_at = Column(DateTime, nullable=False)
    companies_fetched = Column(Integer, nullable=False)
    errors = Column(String, nullable=True)    # JSON string of error details
    duration_ms = Column(Integer, nullable=False)
