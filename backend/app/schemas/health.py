from pydantic import BaseModel


class HealthOut(BaseModel):
    status: str
    cache_age_seconds: float | None = None
    last_scraped_at: str | None = None
    last_scrape_duration_ms: int | None = None
    last_errors: list[str] = []
