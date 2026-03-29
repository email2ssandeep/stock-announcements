Please approve the write permission for `Output/TechArc.md` in the prompt that appeared, then I'll save the document.

The document I've designed covers:

1. **Controllers** — thin HTTP handlers (`announcementController`, `healthController`) that delegate immediately to services
2. **Services** — business logic layer (`announcementService` orchestrates cache → DB → scrape fallback chain; `scraperService` owns Axios + Cheerio)
3. **Repository Pattern** — `announcementRepository` and `scrapeRunRepository` abstract all SQL; services never write raw queries

Plus the full directory structure, data flows (read path + scheduled write path), DB schema, API contract, error handling table, and Railway deployment config — all mapped to the modules from `modules.md`.
