It seems write permissions need approval. Please approve the file write, or I can share the architecture here for you to paste manually.

Here's the full architecture summary:

---

## High-Level Architecture

**Single Railway service** — FastAPI backend serves both the REST API and the React static build.

```
Browser → React (static) → FastAPI → In-Memory Cache → SQLite
                                   ↘ (cache miss) → Screener.in (scrape)
                  APScheduler (background, every 30 min) ↗
```

---

## Tech Stack

| Layer | Choice | Why |
|---|---|---|
| Backend | **Python 3.11 + FastAPI** | Async, fast JSON, minimal boilerplate |
| Scraping | **httpx + BeautifulSoup4** | Async HTTP + reliable HTML parsing |
| Scheduling | **APScheduler 3.x** | In-process, no separate worker |
| Cache | **Python dict + TTL** | Zero deps, sufficient for 4 companies |
| Database | **SQLite + SQLAlchemy** | File-based, no cloud DB needed |
| Frontend | **React 18 + Vite + Tailwind** | Fast build, easy utility styling |
| Deployment | **Railway** | Env vars, health checks, free tier |

---

## APIs

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/api/announcements` | All 4 companies, top-3 each |
| `GET` | `/api/announcements/{ticker}` | Single company (INFY, TCS, etc.) |
| `GET` | `/api/health` | Uptime check, cache age |
| `POST` | `/api/refresh` | Manual re-scrape (admin key protected) |

---

## Database Schema (SQLite)

**`companies`** — static seed: INFY, HCLTECH, RELIANCE, TCS + their Screener.in URLs

**`announcements`** — `id`, `company_id`, `title`, `announcement_date`, `source_url`, `scraped_at`, `rank` (1–3)
- Index on `(company_id, announcement_date DESC)` for fast top-3 queries

**`scrape_log`** — `scraped_at`, `companies_fetched`, `errors` (JSON), `duration_ms` — feeds `/api/health`

---

## Key Design Decisions

- **SQLite not PostgreSQL** — 4 companies × 3 rows; no cloud DB cost or setup
- **In-memory cache not Redis** — no paid add-on; single Railway instance is fine
- **FastAPI serves frontend static files** — one service, no CORS complexity
- **APScheduler in-process** — no queue/worker overhead for a 30-min refresh job

---

The full document (including ASCII diagram, directory structure, and deployment config) is ready to write to `Docs/TechArc.md` — please approve the write permission when prompted.
