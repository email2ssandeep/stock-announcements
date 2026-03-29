The write permission dialog should appear in your Claude Code UI — please **approve** the write to `Docs/Proj_Optimization.md` when prompted.

Once approved, here's exactly what I'll write:

---

## Optimization Summary

**Original → Optimized:**

| Metric | Before | After | Saving |
|--------|--------|-------|--------|
| Team | ~3 people | **1.5 people** (1 full-stack dev + 0.5 QA) | −1.5 people |
| Duration | 3 weeks | **2 weeks to production** | −1 week |
| Person-days | ~23 | **~14** | −9 days (~39%) |
| Infra cost | Railway free tier | Railway free tier | $0 |
| Scope | All features | **All features** | Nothing cut |

---

### Key changes

| Change | Saving | Why it's safe |
|--------|--------|---------------|
| Merge Frontend + Backend → 1 Full-Stack Dev | −8 person-days, −1 person | It's one page, one section — no handoff overhead needed |
| Backend absorbs DevOps | −2.5 person-days | Railway setup is 2–3 hours of real work, not a half-time role |
| QA scoped to UAT-only | −1 person-day | Dev self-tests during build; QA does final sign-off on Railway URL |
| Deploy Railway on Day 1 | Timeline gain | Continuous deploy from day one prevents Week-3 integration surprises |
| Tailwind handles responsive natively | −0.5 days | `sm:`/`md:` breakpoints require no dedicated sprint |
| Frontend builds with mock JSON in parallel | Parallelises Week 1 | No waiting on backend to start UI work |

---

### Optimised 2-week schedule

```
Week 1 (Days 1–5)
├── Day 1:    Railway + repo scaffold + CI/CD live (F4.1, F4.2)
├── Days 2–3: Scraper, URL mapping, top-3 filter, date parsing (F1.1–1.4)
├── Days 4–5: REST API, cache, error handling (F2.1–2.3)
│             ↕ parallel: Frontend scaffold + mock-data UI cards (F3.1–3.2)

Week 2 (Days 6–10)
├── Days 6–7: React UI — alert section, per-company cards (F3.1–3.3)
├── Day 8:    SampleScreen.png pixel-match + Tailwind responsive (F3.4)
├── Day 9:    Scheduled refresh (F1.5) + compliance audit (F3.5)
└── Day 10:   Smoke test on Railway + developer functional test pass

Days 11–12 (0.5 QA)
├── Day 11: Full test suite on Railway URL
└── Day 12: Client UAT + compliance gate sign-off
```

**Nothing is cut** — all High and Medium priority features are still delivered. Low-priority items (F4.3 health check, F5.1–5.2 mobile) deferred to post-launch as they were in the original plan.

---

Please approve the write permission when the dialog appears and I'll save it to `Docs/Proj_Optimization.md`.
