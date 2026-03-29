Please approve the write permission to save `Output/TechArc.md`, and I'll proceed.

Here's a summary of the architecture I've designed:

---

## Architecture Overview

**Style:** Single-process monolith on Railway — one Node.js service hosts both the API and the React SPA. No microservices needed at this scale.

### Tech Stack

| Layer | Choice |
|-------|--------|
| Runtime | Node.js 20 LTS |
| Web Framework | Express 4 |
| Scraping | Axios (HTTP) + Cheerio (HTML parse) |
| Scheduler | node-cron |
| Database | SQLite via `better-sqlite3` |
| Cache | Plain JS `Map` (in-memory) |
| Frontend | React 18 + Vite + Tailwind CSS |
| Deploy | Railway (single service) |

### APIs

**External:** HTTP scrape of 4 Screener.in company pages — no official API exists.

**Internal REST:**
- `GET /api/announcements` — all 4 companies × 3 entries, with `stale` flag if serving cached data
- `GET /api/announcements/:ticker` — single company
- `GET /api/health` — Railway liveness probe

### Database Schema (SQLite)

Two tables:
- **`announcements`** — stores current 12 rows (4 companies × 3); unique index on `(ticker, rank)` handles upserts cleanly
- **`scrape_runs`** — audit log per scrape attempt with `status`, `companies_ok`, `companies_err`

### Critical Path
```
Scraper (M1) → REST API (M2-F1) → React Dashboard (M3) → Railway Deploy (M4)
```

The SQLite layer serves as the fallback when Screener.in is unreachable — the in-memory cache is fast-path, SQLite is the safety net across restarts.
