Here's the BRD broken into modules and features with priority:

---

## Module Breakdown

### Module 1 — Data Scraping Layer `[HIGH]`
| Feature | Description | Priority |
|---|---|---|
| F1.1 Screener.in scraper | Fetch announcement data from Screener.in for each company | **High** |
| F1.2 Company URL mapping | Map Infosys, HCL, Reliance, TCS to their Screener.in profile URLs | **High** |
| F1.3 Top-3 filter | Retain only the 3 most recent announcements per company | **High** |
| F1.4 Date extraction | Parse and normalize announcement date from each entry | **High** |
| F1.5 Scheduled refresh | Periodically re-fetch data to keep announcements current | **Medium** |

---

### Module 2 — Backend / API Layer `[HIGH]`
| Feature | Description | Priority |
|---|---|---|
| F2.1 Announcements API endpoint | Serve scraped announcement data as JSON to the frontend | **High** |
| F2.2 Data caching | Cache scraper results to reduce repeated hits on Screener.in | **Medium** |
| F2.3 Error handling | Graceful fallback if Screener.in is unreachable or page structure changes | **Medium** |

---

### Module 3 — Frontend Dashboard `[HIGH]`
| Feature | Description | Priority |
|---|---|---|
| F3.1 Announcement Alert Section | Dedicated UI section showing announcements for all 4 companies | **High** |
| F3.2 Per-company announcement cards | Display up to 3 entries per company with date first | **High** |
| F3.3 UI styling (SampleScreen.png match) | Visual design matches the provided reference screen | **High** |
| F3.4 Responsive layout | Dashboard usable on desktop browsers | **Medium** |
| F3.5 No share price display | Ensure no price data surfaces anywhere in the UI | **High** (compliance) |

---

### Module 4 — Deployment `[HIGH]`
| Feature | Description | Priority |
|---|---|---|
| F4.1 Railway deployment | App deployed and publicly accessible via Railway URL | **High** |
| F4.2 Environment configuration | Manage config/secrets for Railway environment | **Medium** |
| F4.3 Health check / uptime | Basic Railway service health monitoring | **Low** |

---

### Module 5 — Mobile App Feasibility `[LOW]`
| Feature | Description | Priority |
|---|---|---|
| F5.1 Feasibility assessment | Evaluate converting web app to mobile (PWA, React Native, etc.) | **Low** |
| F5.2 Architecture recommendations | Document approach if conversion is greenlit | **Low** |

---

## Summary by Priority

| Priority | Features |
|---|---|
| **High** | F1.1–1.4, F2.1, F3.1–3.3, F3.5, F4.1 |
| **Medium** | F1.5, F2.2–2.3, F3.4, F4.2 |
| **Low** | F4.3, F5.1–5.2 |

---

**Critical path for initial release:** Module 1 → Module 2 → Module 3 → Module 4 (all High priority items). Module 5 is post-launch only.

Shall I write this breakdown to `Docs\brd.md` or a separate file like `Docs\modules.md`?
