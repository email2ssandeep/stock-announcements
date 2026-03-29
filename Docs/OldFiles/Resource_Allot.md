# Resource Allocation Plan — Stock Announcements Dashboard

---

## Team Composition

| # | Role | Headcount | Type |
|---|------|-----------|------|
| 1 | Full-Stack Developer | 1 | Core |
| 2 | Frontend Developer | 1 | Core |
| 3 | DevOps / Deployment Engineer | 1 | Core (part-time) |
| 4 | QA / Tester | 1 | Shared / part-time |

**Total: 3–4 people** (lean team; DevOps and QA can be shared resources)

---

## Role Details

---

### Role 1 — Full-Stack Developer
**Headcount:** 1

**Responsibilities:**
- Build the Screener.in HTTP scraper (M1-F1)
- Write the HTML announcement parser (M1-F2)
- Implement the latest-3 filter logic (M1-F3)
- Define and own the data model `{company, date, title, url}` (M1-F4)
- Build the `/api/announcements` REST endpoint (M2-F1)
- Implement scheduled re-scrape (M2-F2)
- Build in-memory cache layer (M2-F3)
- Implement per-company error handling and fallback (M2-F4)

**Timeline:**

| Phase | Tasks | Duration |
|-------|-------|----------|
| Week 1 | M1-F1, M1-F2, M1-F3, M1-F4 — scraper + parser + data model | 5 days |
| Week 2 | M2-F1 — REST API endpoint, wire up to parsed data | 2 days |
| Week 2 | M2-F3, M2-F4 — cache + error handling | 2 days |
| Week 3 | M2-F2 — scheduled refresh; backend integration testing | 1 day |

**Total: ~10 working days**

---

### Role 2 — Frontend Developer
**Headcount:** 1

**Responsibilities:**
- Build the Announcement Alert Section UI (M3-F1)
- Implement per-entry date-first layout (M3-F2)
- Build company grouping / labeling logic (M3-F3)
- Match visual styling to `SampleScreen.png` — colors, fonts, layout (M3-F4)
- Implement responsive layout for desktop + baseline mobile (M3-F5)
- Consume `/api/announcements` and handle loading/error states

**Timeline:**

| Phase | Tasks | Duration |
|-------|-------|----------|
| Week 1 | Review `SampleScreen.png`, set up project scaffold, static mockup | 2 days |
| Week 2 | M3-F1, M3-F2, M3-F3 — live data rendering, grouping, layout | 3 days |
| Week 2–3 | M3-F4 — pixel-match styling to sample screen | 2 days |
| Week 3 | M3-F5 — responsive layout, cross-browser check | 1 day |

**Note:** Frontend work on the static mockup can begin in Week 1 in parallel with backend — no blocker until the API is ready (end of Week 2).

**Total: ~8 working days**

---

### Role 3 — DevOps / Deployment Engineer
**Headcount:** 1 (part-time, ~30% allocation)

**Responsibilities:**
- Set up Railway project and service (M4-F1)
- Configure environment variables and start command (M4-F1, M4-F3)
- Validate public URL is live (M4-F2)
- Externalize configurable values: refresh interval, company list (M4-F3)
- Support CI/CD if needed; assist with production smoke tests

**Timeline:**

| Phase | Tasks | Duration |
|-------|-------|----------|
| Week 1 | Railway project creation, env var skeleton, repo link | 1 day |
| Week 3 | Full deployment once frontend + backend are integrated | 1 day |
| Week 3 | Smoke test on live URL, env config validation | 0.5 days |

**Total: ~2.5 working days** (spread across the project)

---

### Role 4 — QA / Tester
**Headcount:** 1 (part-time, shared resource)

**Responsibilities:**
- Verify scraper output matches live Screener.in data
- Test API endpoint responses for all 4 companies
- Validate fallback behavior when Screener.in is unreachable
- Validate UI rendering matches `SampleScreen.png`
- Cross-browser and basic mobile responsiveness checks
- Sign off on Railway-hosted production URL

**Timeline:**

| Phase | Tasks | Duration |
|-------|-------|----------|
| Week 2 | Backend API testing — response structure, edge cases | 1 day |
| Week 3 | Frontend UI testing — layout, grouping, styling | 1 day |
| Week 3 | End-to-end test on Railway production URL | 0.5 days |

**Total: ~2.5 working days**

---

## Master Timeline

```
Week 1 (Days 1–5)
├── Full-Stack Dev:   M1-F1 → M1-F2 → M1-F3 → M1-F4  [scraper + parser]
├── Frontend Dev:     SampleScreen review + static UI mockup
└── DevOps:           Railway project setup (Day 1, ~1 day)

Week 2 (Days 6–10)
├── Full-Stack Dev:   M2-F1 + M2-F3 + M2-F4  [API + cache + error handling]
├── Frontend Dev:     M3-F1 + M3-F2 + M3-F3  [live data + grouping]
└── QA:               Backend API testing (Days 9–10)

Week 3 (Days 11–15)
├── Full-Stack Dev:   M2-F2  [scheduled refresh] + integration support
├── Frontend Dev:     M3-F4 + M3-F5  [styling + responsive]
├── DevOps:           Railway deploy + env config (Day 13–14)
└── QA:               UI testing + E2E on production URL (Days 14–15)
```

---

## Summary

| Role | Days | Critical Path Owner |
|------|------|---------------------|
| Full-Stack Developer | 10 | Yes — M1 + M2 block everything |
| Frontend Developer | 8 | Yes — M3 blocks deploy |
| DevOps Engineer | 2.5 | Yes — M4 is the final gate |
| QA / Tester | 2.5 | No — validates, doesn't block |
| **Total effort** | **~23 person-days** | **3-week delivery** |

---

**Critical path:** Full-Stack Dev (M1 scraper) → Full-Stack Dev (M2 API) → Frontend Dev (M3 UI) → DevOps (M4 Railway deploy) → QA sign-off.
