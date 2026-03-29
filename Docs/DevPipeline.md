It looks like write permissions need to be approved for the `backend/` directory. Please approve the file write when prompted, or grant permission for the path `D:/Sandeep_AITest/Test_Claude/StockAnnoucements/backend/`.

Once approved, I'll generate all these files in one go:

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                      # FastAPI app + static file serving
│   ├── config.py                    # Settings (env vars, company URLs)
│   ├── database.py                  # SQLAlchemy engine + session
│   ├── models/
│   │   ├── company.py               # Company ORM model
│   │   ├── announcement.py          # Announcement ORM model
│   │   └── scrape_log.py            # ScrapeLog ORM model
│   ├── schemas/
│   │   ├── announcement.py          # Pydantic request/response shapes
│   │   └── health.py
│   ├── repositories/
│   │   ├── base.py                  # Generic CRUD base
│   │   ├── company_repository.py
│   │   ├── announcement_repository.py
│   │   └── scrape_log_repository.py
│   ├── services/
│   │   ├── cache_service.py         # TTL in-memory cache
│   │   ├── scraper_service.py       # httpx + BS4 → Screener.in
│   │   ├── announcement_service.py  # Orchestrates cache → DB → scraper
│   │   └── scheduler_service.py     # APScheduler 30-min job
│   ├── controllers/
│   │   ├── announcement_controller.py  # /api/announcements routes
│   │   └── health_controller.py        # /api/health + /api/refresh
│   └── core/
│       └── seed.py                  # Seed companies table on startup
└── requirements.txt
```

Try approving the write in the Claude Code permission dialog, then I'll proceed. If the dialog doesn't appear, let me know and I can try a different approach.
