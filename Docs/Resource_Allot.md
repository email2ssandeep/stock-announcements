## Resource Allocation Plan

---

### Roles & Team Composition

| # | Role | Headcount | Modules Owned |
|---|---|---|---|
| 1 | Backend Engineer | 1 | M1 (Scraping), M2 (API) |
| 2 | Frontend Engineer | 1 | M3 (Dashboard) |
| 3 | DevOps / Deployment | 0.5 *(shared)* | M4 (Railway) |
| 4 | QA / Tester | 0.5 *(shared)* | All modules |
| **Total** | | **~3 people** | |

> For a lean team, Backend Engineer doubles as DevOps; Frontend Engineer doubles as QA on their own work. Minimum viable: **2 engineers** with split responsibilities.

---

### Responsibilities per Role

#### Backend Engineer
- F1.1 — Build Screener.in scraper (HTML parsing / HTTP client)
- F1.2 — Maintain company → URL mapping config
- F1.3 — Implement top-3 filter logic
- F1.4 — Date parsing and normalization
- F1.5 — Scheduled refresh (cron job or background task)
- F2.1 — Build `/announcements` REST API endpoint
- F2.2 — Implement in-memory or file-based caching layer
- F2.3 — Add error handling, fallback responses
- F4.2 — Configure Railway environment variables / secrets

#### Frontend Engineer
- F3.1 — Build Announcement Alert section component
- F3.2 — Per-company announcement card components (date-first layout)
- F3.3 — Style to match `SampleScreen.png` reference
- F3.4 — Responsive layout for desktop browsers
- F3.5 — Audit UI to ensure zero price data surfaces (compliance check)

#### DevOps *(Backend Engineer or shared)*
- F4.1 — Railway project setup, deploy pipeline, public URL
- F4.3 — Configure health check / uptime monitor

#### QA *(shared or Frontend Engineer)*
- End-to-end test: scraper → API → UI rendering
- Verify top-3 filter correctness per company
- Compliance check: confirm no share price in UI
- Regression after each deployment

---

### Timeline per Role

Assuming a **2-week sprint** to initial release (all High priority items):

```
Week 1                          Week 2
Mon  Tue  Wed  Thu  Fri  |  Mon  Tue  Wed  Thu  Fri
```

| Role | Days 1–3 | Days 4–5 | Days 6–8 | Days 9–10 |
|---|---|---|---|---|
| **Backend** | F1.1, F1.2 (scraper + URL mapping) | F1.3, F1.4 (filter + date parse) | F2.1, F2.3 (API + error handling) | F1.5, F2.2 (scheduler + cache) |
| **Frontend** | F3.3 setup (project scaffold + style baseline) | F3.1, F3.2 (alert section + cards) | F3.5 compliance review + F3.4 responsive | Integration with live API, polish |
| **DevOps/QA** | — | Railway project setup (F4.1, F4.2) | Integration smoke tests | Full QA pass, F4.3 health check |

---

### Post-Launch (Week 3+)

| Role | Work |
|---|---|
| Backend | Monitor scraper stability, patch if Screener.in HTML changes |
| Frontend | Address any UI feedback |
| DevOps | Uptime monitoring, Railway alerts |
| Both | F5.1–F5.2 mobile feasibility assessment (low priority) |

---

### Critical Path

```
[F1.1 Scraper] → [F2.1 API] → [F3.1–3.2 UI Cards] → [F4.1 Deploy]
```

Backend scraper must be functional before Frontend can integrate real data. Frontend can build with mock JSON in parallel during Week 1.
