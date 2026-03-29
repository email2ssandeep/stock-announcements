## Modules & Features Breakdown

---

### Module 1 — Data Layer
**Purpose:** Fetch and parse announcement data from Screener.in

| Feature | Description | Priority |
|---------|-------------|----------|
| M1-F1: Screener.in Scraper | HTTP client to fetch company pages for Infosys, HCL, Reliance, TCS | **High** |
| M1-F2: Announcement Parser | Extract announcement date + text from page HTML | **High** |
| M1-F3: Latest-3 Filter | Retain only the 3 most recent announcements per company | **High** |
| M1-F4: Data Model | Structured object: `{company, date, title, url}` per announcement | **High** |

---

### Module 2 — Backend / API
**Purpose:** Serve parsed data to the frontend

| Feature | Description | Priority |
|---------|-------------|----------|
| M2-F1: REST Endpoint | `/api/announcements` returns all 4 companies × 3 announcements | **High** |
| M2-F2: Scheduled Refresh | Periodic re-scrape to keep data current (e.g., every 30 min) | **Medium** |
| M2-F3: In-memory Cache | Serve last-known data if Screener.in is temporarily unreachable | **Medium** |
| M2-F4: Error Handling | Graceful fallback if scraping fails for one or more companies | **Medium** |

---

### Module 3 — Frontend / Dashboard UI
**Purpose:** Display announcements per `SampleScreen.png` design

| Feature | Description | Priority |
|---------|-------------|----------|
| M3-F1: Announcement Alert Section | Dedicated section listing all company announcements | **High** |
| M3-F2: Per-Entry Layout | Date shown first, followed by announcement text | **High** |
| M3-F3: Company Grouping | Announcements visually grouped or labeled by company | **High** |
| M3-F4: UI Styling | Match visual style from `SampleScreen.png` (colors, fonts, layout) | **High** |
| M3-F5: Responsive Layout | Usable on desktop browsers; baseline mobile-friendly HTML | **Medium** |

---

### Module 4 — Deployment
**Purpose:** Host and run the application on Railway

| Feature | Description | Priority |
|---------|-------------|----------|
| M4-F1: Railway Project Setup | Configure Railway service, environment variables, start command | **High** |
| M4-F2: Public URL | App accessible via Railway-provided domain | **High** |
| M4-F3: Environment Config | Externalize any configurable values (refresh interval, company list) | **Medium** |

---

### Module 5 — Mobile Feasibility (Future)
**Purpose:** Evaluate post-launch mobile conversion

| Feature | Description | Priority |
|---------|-------------|----------|
| M5-F1: Tech Assessment | Evaluate React Native / Flutter / PWA conversion options | **Low** |
| M5-F2: PWA Baseline | Add `manifest.json` + service worker to web app for installability | **Low** |

---

### Priority Summary

| Priority | Count | Items |
|----------|-------|-------|
| **High** | 11 | Core scraping, parsing, API, UI display, Railway deploy |
| **Medium** | 6 | Caching, refresh scheduling, error handling, responsive layout, env config |
| **Low** | 2 | Mobile feasibility study, PWA baseline |

---

**Critical path:** M1 (scraper + parser) → M2-F1 (API endpoint) → M3 (dashboard UI) → M4 (Railway deploy). Everything else is enhancement or future work.
