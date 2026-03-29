import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.database import Base, get_db
from app.main import app
from app.core.seed import seed_companies
from app.models.announcement import Announcement
from app.models.scrape_log import ScrapeLog
from app.services import cache_service

TEST_DB_URL = "sqlite:///./test_announcements.db"


@pytest.fixture(scope="session")
def engine():
    eng = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=eng)
    yield eng
    Base.metadata.drop_all(bind=eng)
    import os
    try:
        if os.path.exists("test_announcements.db"):
            os.remove("test_announcements.db")
    except PermissionError:
        pass  # Windows may hold file lock briefly; safe to ignore in CI


@pytest.fixture(scope="function")
def db(engine):
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = Session()
    seed_companies(session)
    yield session
    session.query(Announcement).delete()
    session.query(ScrapeLog).delete()
    session.commit()
    session.close()


@pytest.fixture(scope="function")
def client(db):
    """TestClient with test DB injected, cache cleared, and startup scrape mocked."""
    from unittest.mock import patch
    cache_service._store.clear()

    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    # Prevent lifespan from hitting Screener.in during test startup
    with patch("app.services.announcement_service.refresh_announcements", return_value={}):
        with TestClient(app, raise_server_exceptions=True) as c:
            yield c

    app.dependency_overrides.clear()
    cache_service._store.clear()


# ── Reusable sample announcement data ──────────────────────────────────────

SAMPLE_ANNOUNCEMENTS = {
    "infosys": [
        {"date": "25 Mar", "title": "Acquisition — Infosys to acquire HealthIT for $465m", "source_url": "https://bseindia.com/doc1.pdf"},
        {"date": "24 Mar", "title": "Results — Q4 FY2026 results announced", "source_url": "https://bseindia.com/doc2.pdf"},
        {"date": "20 Mar", "title": "Dividend — Board recommends interim dividend", "source_url": "https://bseindia.com/doc3.pdf"},
    ],
    "hcl": [
        {"date": "25 Mar", "title": "Award — HCL wins $500m deal with US bank", "source_url": "https://bseindia.com/doc4.pdf"},
        {"date": "24 Mar", "title": "Closure of Trading Window — March 2026", "source_url": "https://bseindia.com/doc5.pdf"},
        {"date": "22 Mar", "title": "Board Meeting — April 20 2026 financial results", "source_url": "https://bseindia.com/doc6.pdf"},
    ],
    "reliance": [
        {"date": "28 Mar", "title": "Statement — Reliance denies Iranian crude reports", "source_url": "https://bseindia.com/doc7.pdf"},
        {"date": "18 Mar", "title": "Customs — Redemption fine Rs.17,06,958 order", "source_url": "https://bseindia.com/doc8.pdf"},
        {"date": "16 Mar", "title": "Green Ammonia — Binding offtake agreement with Samsung", "source_url": "https://bseindia.com/doc9.pdf"},
    ],
    "tcs": [
        {"date": "28 Mar", "title": "Investor Meet — Analyst meeting intimation", "source_url": "https://bseindia.com/doc10.pdf"},
        {"date": "23 Mar", "title": "Board Meeting — FY2026 audited results April 9", "source_url": "https://bseindia.com/doc11.pdf"},
        {"date": "20 Mar", "title": "Partnership — TCS and Swissport extend strategic deal", "source_url": "https://bseindia.com/doc12.pdf"},
    ],
}


@pytest.fixture
def seeded_db(db):
    """DB with announcement rows pre-populated for all 4 companies."""
    from app.repositories.company_repository import CompanyRepository
    from app.repositories.announcement_repository import AnnouncementRepository

    company_repo = CompanyRepository(db)
    ann_repo = AnnouncementRepository(db)

    for ticker, items in SAMPLE_ANNOUNCEMENTS.items():
        company = company_repo.get_by_ticker(ticker)
        new_anns = [
            Announcement(
                company_id=company.id,
                title=item["title"],
                announcement_date=item["date"],
                source_url=item["source_url"],
                scraped_at=datetime.utcnow(),
                rank=idx + 1,
            )
            for idx, item in enumerate(items)
        ]
        ann_repo.replace_for_company(company.id, new_anns)

    return db


@pytest.fixture
def seeded_client(seeded_db):
    """TestClient backed by a fully seeded test database."""
    cache_service._store.clear()

    def override_get_db():
        yield seeded_db

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app, raise_server_exceptions=True) as c:
        yield c

    app.dependency_overrides.clear()
    cache_service._store.clear()
