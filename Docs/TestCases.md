## Test Documentation

### Functional Test Cases

---

**Module 1 — Data Scraping Layer**

| TC ID | Feature | Test Case | Steps | Expected Result | Priority |
|---|---|---|---|---|---|
| TC-F1.1-01 | F1.1 Scraper | Scrape Screener.in for Infosys | Trigger scraper for Infosys URL | Returns list of announcement objects with title + date | High |
| TC-F1.1-02 | F1.1 Scraper | Scrape all 4 companies | Run scraper for Infosys, HCL, Reliance, TCS | All 4 companies return data | High |
| TC-F1.2-01 | F1.2 URL Mapping | URL mapping loads correctly | Read company-to-URL config | All 4 companies have valid Screener.in profile URLs | High |
| TC-F1.2-02 | F1.2 URL Mapping | No company missing from mapping | Assert keys in map | Exactly: Infosys, HCL, Reliance, TCS | High |
| TC-F1.3-01 | F1.3 Top-3 Filter | Filter returns at most 3 items | Fetch company with 10+ announcements | Only 3 returned | High |
| TC-F1.3-02 | F1.3 Top-3 Filter | Filter returns most recent 3 | Fetch company data | Items are ordered newest-first, oldest is item [2] | High |
| TC-F1.3-03 | F1.3 Top-3 Filter | Company with fewer than 3 announcements | Simulate company with 1 announcement | Returns 1 item (no padding/error) | High |
| TC-F1.4-01 | F1.4 Date Extraction | Date parsed from announcement | Inspect scraped item | `date` field is a valid normalized date string | High |
| TC-F1.4-02 | F1.4 Date Extraction | Date ordering is correct | Compare dates across 3 items | date[0] >= date[1] >= date[2] | High |
| TC-F1.5-01 | F1.5 Scheduled Refresh | Refresh updates stale data | Wait for refresh interval, check cache timestamp | Cache timestamp updated, content may differ | Medium |

---

**Module 2 — Backend / API Layer**

| TC ID | Feature | Test Case | Steps | Expected Result | Priority |
|---|---|---|---|---|---|
| TC-F2.1-01 | F2.1 API Endpoint | GET /announcements returns 200 | Call GET /api/announcements | HTTP 200, JSON body | High |
| TC-F2.1-02 | F2.1 API Endpoint | Response contains all 4 companies | Parse response body | Keys/entries for Infosys, HCL, Reliance, TCS present | High |
| TC-F2.1-03 | F2.1 API Endpoint | Each company has ≤3 announcements | Inspect response | `announcements.length <= 3` per company | High |
| TC-F2.1-04 | F2.1 API Endpoint | Each announcement has title + date | Inspect announcement objects | `title` and `date` fields present and non-empty | High |
| TC-F2.2-01 | F2.2 Caching | Second call uses cache | Call API twice; compare timestamps | Second response faster; scraper not re-invoked | Medium |
| TC-F2.2-02 | F2.2 Caching | Cache invalidates after TTL | Wait for TTL expiry, call again | Fresh scrape triggered after expiry | Medium |
| TC-F2.3-01 | F2.3 Error Handling | Screener.in unreachable | Mock network failure | API returns 503 or cached fallback, no 500 crash | Medium |
| TC-F2.3-02 | F2.3 Error Handling | Screener.in HTML structure changes | Mock scraper returning empty list | API returns graceful empty/error response, not exception | Medium |

---

**Module 3 — Frontend Dashboard**

| TC ID | Feature | Test Case | Steps | Expected Result | Priority |
|---|---|---|---|---|---|
| TC-F3.1-01 | F3.1 Alert Section | Announcement section renders | Load dashboard | "Announcement Alert" section visible on page | High |
| TC-F3.1-02 | F3.1 Alert Section | All 4 companies shown | Load dashboard | Infosys, HCL, Reliance, TCS each have a section | High |
| TC-F3.2-01 | F3.2 Cards | Date displayed first on card | Inspect announcement card | Date appears before announcement title text | High |
| TC-F3.2-02 | F3.2 Cards | Up to 3 cards per company | Count cards per company | Card count is 1–3 per company | High |
| TC-F3.3-01 | F3.3 UI Styling | Visual matches reference screen | Compare to SampleScreen.png | Layout, colors, card structure match reference | High |
| TC-F3.4-01 | F3.4 Responsive | Dashboard renders on 1280px viewport | Open in desktop browser at 1280px | No horizontal scroll, all content visible | Medium |
| TC-F3.5-01 | F3.5 No Price Data | No share price visible | Inspect entire dashboard | Zero price/₹/$ values visible anywhere on screen | High |
| TC-F3.5-02 | F3.5 No Price Data | API response contains no price fields | Inspect /api/announcements JSON | No `price`, `close`, `open`, `volume` fields in response | High |

---

**Module 4 — Deployment**

| TC ID | Feature | Test Case | Steps | Expected Result | Priority |
|---|---|---|---|---|---|
| TC-F4.1-01 | F4.1 Railway Deploy | App accessible via Railway URL | Open Railway public URL | Dashboard loads, no 404/502 | High |
| TC-F4.1-02 | F4.1 Railway Deploy | API reachable on Railway | GET Railway URL /api/announcements | 200 with valid JSON | High |
| TC-F4.2-01 | F4.2 Env Config | App reads env vars correctly | Deploy with Railway env vars set | App starts without missing config errors | Medium |

---

### API Test Cases

| TC ID | Method | Endpoint | Input | Expected Status | Expected Body |
|---|---|---|---|---|---|
| API-01 | GET | `/api/announcements` | None | 200 | `{ "infosys": [...], "hcl": [...], "reliance": [...], "tcs": [...] }` |
| API-02 | GET | `/api/announcements` | None | 200 | Each array has length 1–3 |
| API-03 | GET | `/api/announcements` | None | 200 | Each item has `"title"` (non-empty string) |
| API-04 | GET | `/api/announcements` | None | 200 | Each item has `"date"` (non-empty, parseable date string) |
| API-05 | GET | `/api/announcements` | None | 200 | No `price`, `ltp`, `volume`, or financial metric fields |
| API-06 | GET | `/api/announcements` | Screener.in mocked as down | 503 or 200 with cached | Graceful response, no stack trace in body |
| API-07 | GET | `/api/announcements` | Scraper returns empty | 200 | `{ "infosys": [], ... }` or specific error message |
| API-08 | GET | `/api/announcements` | Called twice within TTL | 200 | Both return identical data; response time drops on 2nd call |
| API-09 | GET | `/api/health` (if exists) | None | 200 | `{ "status": "ok" }` or equivalent |
| API-10 | GET | `/api/announcements` | Invalid/unknown path | 404 | Standard not-found response |

---

### Edge Cases

**Scraping**
- Screener.in returns 0 announcements for a company → app does not crash, returns empty list
- Screener.in returns 1 or 2 announcements (fewer than 3) → only those items shown, no blank padding
- Announcement has no date field or malformed date → date shown as `"N/A"` or item skipped with logging
- Announcement title contains special characters (`<`, `>`, `&`, `"`) → escaped properly in JSON and rendered safely in UI
- Screener.in changes its HTML structure → scraper fails gracefully with logged warning, last cached data served
- Network timeout during scrape → timeout handled, fallback to cache if available

**API**
- Concurrent requests to `/api/announcements` → both served correctly, no race condition on cache write
- Cache is empty and Screener.in is down simultaneously → returns 503 or structured error, not a 500
- Very large announcement title (>500 chars) → truncated or handled without breaking layout
- Date string in unexpected locale/format → normalized or flagged, no silent data corruption

**Frontend**
- API returns empty array for one company → company section shows a "No announcements" message, not broken layout
- API call fails entirely → dashboard shows error state, does not render blank cards
- Announcement title is very long → text wraps or truncates without breaking card width
- Browser zoom at 150% → layout does not overflow or overlap
- Dashboard loaded with slow network (3G throttle) → page still usable; no blank white screen

**Compliance**
- Any future API field accidentally includes price data → F3.5 regression test catches it
- Screener.in page includes price in announcement text → displayed as-is (text only), but no structured price field exposed

---

### UAT Checklist

**Module 1 — Scraping**
- [ ] Announcements are fetched for all 4 companies: Infosys, HCL, Reliance, TCS
- [ ] Only the 3 most recent announcements per company are shown
- [ ] Announcements are ordered newest-first
- [ ] Each announcement has a visible, correctly formatted date
- [ ] Data refreshes periodically without manual intervention

**Module 2 — Backend**
- [ ] `/api/announcements` returns valid JSON within acceptable response time (<3s)
- [ ] API does not expose any share price or financial metric data
- [ ] If Screener.in is unreachable, the app does not crash or show a raw error
- [ ] Cached data is served on repeated requests within TTL window

**Module 3 — Frontend**
- [ ] Dashboard loads in a desktop browser without errors
- [ ] "Announcement Alert" section is clearly visible and labeled
- [ ] All 4 companies have their own section/card group
- [ ] Each announcement card shows the date before the title
- [ ] No price, stock value, or financial figure appears anywhere on screen
- [ ] Visual layout matches SampleScreen.png reference (layout, card style, colors)
- [ ] No broken UI when one company has fewer than 3 announcements
- [ ] No horizontal scrollbar at 1280px desktop width

**Module 4 — Deployment**
- [ ] App is publicly accessible via Railway URL
- [ ] API endpoint works on Railway (not just localhost)
- [ ] No credentials or secrets are hardcoded in the deployed code
- [ ] App restarts cleanly after Railway redeploy

**Compliance Gate (sign-off required)**
- [ ] Confirmed: zero share price data visible in UI
- [ ] Confirmed: zero share price data in API response
- [ ] Confirmed: only announcement text and dates are surfaced

---

Want me to write these to a file like `Docs\test_cases.md`?
