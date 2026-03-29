# Test Plan: Stock Announcements Dashboard

---

## 1. Functional Test Cases

### Module 1 — Data Layer

| TC ID | Feature | Test Case | Input | Expected Result | Pass/Fail |
|-------|---------|-----------|-------|-----------------|-----------|
| M1-F1-TC01 | Scraper | Fetch Infosys page successfully | Valid Infosys URL | HTTP 200, HTML body returned | |
| M1-F1-TC02 | Scraper | Fetch HCL page successfully | Valid HCL URL | HTTP 200, HTML body returned | |
| M1-F1-TC03 | Scraper | Fetch Reliance page successfully | Valid Reliance URL | HTTP 200, HTML body returned | |
| M1-F1-TC04 | Scraper | Fetch TCS page successfully | Valid TCS URL | HTTP 200, HTML body returned | |
| M1-F1-TC05 | Scraper | All 4 companies fetched in single run | Trigger scrape | 4 company datasets returned, none null | |
| M1-F2-TC01 | Parser | Extract announcement date | Raw HTML with announcements | Date in expected format (e.g., `DD Mon YYYY`) | |
| M1-F2-TC02 | Parser | Extract announcement text/title | Raw HTML with announcements | Non-empty string, no HTML tags in output | |
| M1-F2-TC03 | Parser | Parse multiple announcements | HTML with 5+ announcements | All announcements extracted as list | |
| M1-F2-TC04 | Parser | Handle missing date field | HTML with announcement lacking date | Graceful skip or null date, no crash | |
| M1-F3-TC01 | Latest-3 Filter | Filter to 3 most recent | 5 announcements for a company | Only 3 returned, in descending date order | |
| M1-F3-TC02 | Latest-3 Filter | Exactly 3 announcements available | 3 announcements in source | All 3 returned, none dropped | |
| M1-F3-TC03 | Latest-3 Filter | Fewer than 3 announcements | 1–2 announcements in source | All available returned (no error) | |
| M1-F4-TC01 | Data Model | Object shape validation | Parsed announcement | Contains `company`, `date`, `title`, `url` fields | |
| M1-F4-TC02 | Data Model | Company field correct | Infosys announcement | `company` = `"Infosys"` | |
| M1-F4-TC03 | Data Model | URL field populated | Parsed announcement | `url` is non-empty, valid format | |

---

### Module 2 — Backend / API

| TC ID | Feature | Test Case | Input | Expected Result | Pass/Fail |
|-------|---------|-----------|-------|-----------------|-----------|
| M2-F1-TC01 | REST Endpoint | GET `/api/announcements` returns 200 | Valid GET request | HTTP 200 | |
| M2-F1-TC02 | REST Endpoint | Response contains all 4 companies | GET `/api/announcements` | 4 company groups in response | |
| M2-F1-TC03 | REST Endpoint | Each company has 3 announcements | GET `/api/announcements` | 12 total announcement objects | |
| M2-F1-TC04 | REST Endpoint | Response is valid JSON | GET `/api/announcements` | `Content-Type: application/json`, parseable body | |
| M2-F2-TC01 | Scheduled Refresh | Refresh triggers on schedule | Wait for refresh interval (30 min) | Data timestamp updated, new data fetched | |
| M2-F2-TC02 | Scheduled Refresh | Refresh does not break running server | Trigger refresh mid-request | Server continues serving requests | |
| M2-F3-TC01 | Cache | Serve cached data when Screener.in unreachable | Mock Screener.in down | API returns last known data, HTTP 200 | |
| M2-F3-TC02 | Cache | Cache populated on first scrape | Cold start + scrape | Subsequent requests served from cache | |
| M2-F4-TC01 | Error Handling | One company scrape fails | Mock Infosys fetch failure | Other 3 companies still returned; Infosys entry absent or flagged | |
| M2-F4-TC02 | Error Handling | All companies fail | Mock all fetches fail | API returns cached data or empty list with error flag, no 500 crash | |

---

### Module 3 — Frontend / Dashboard UI

| TC ID | Feature | Test Case | Steps | Expected Result | Pass/Fail |
|-------|---------|-----------|-------|-----------------|-----------|
| M3-F1-TC01 | Alert Section | Announcement section renders | Load dashboard | Announcement Alert section visible on page | |
| M3-F1-TC02 | Alert Section | Data loads on page load | Open dashboard | Announcements populated within 3 seconds | |
| M3-F2-TC01 | Per-Entry Layout | Date displayed first | Inspect each entry | Date appears above/before announcement text | |
| M3-F2-TC02 | Per-Entry Layout | Announcement text displayed | Inspect each entry | Title/text visible, not truncated unexpectedly | |
| M3-F3-TC01 | Company Grouping | Companies visually separated | View dashboard | Clear label or divider for each company | |
| M3-F3-TC02 | Company Grouping | All 4 companies present | View dashboard | Infosys, HCL, Reliance, TCS all shown | |
| M3-F4-TC01 | UI Styling | Colors match design | Compare to `SampleScreen.png` | Background, text, and accent colors match | |
| M3-F4-TC02 | UI Styling | Font style matches | Compare to `SampleScreen.png` | Font family/size consistent with design | |
| M3-F5-TC01 | Responsive Layout | Desktop browser display | Open at 1280×800 | No horizontal scroll, layout intact | |
| M3-F5-TC02 | Responsive Layout | Mobile viewport | Open at 375×812 | Content readable, no overflow | |

---

### Module 4 — Deployment

| TC ID | Feature | Test Case | Steps | Expected Result | Pass/Fail |
|-------|---------|-----------|-------|-----------------|-----------|
| M4-F1-TC01 | Railway Setup | Service starts successfully | Deploy to Railway | Build logs show success, no startup errors | |
| M4-F1-TC02 | Railway Setup | Environment variables set | Check Railway config | All required env vars present | |
| M4-F2-TC01 | Public URL | App reachable via Railway domain | Open Railway URL | Dashboard loads successfully | |
| M4-F2-TC02 | Public URL | API reachable externally | GET `<railway-url>/api/announcements` | HTTP 200 with JSON data | |
| M4-F3-TC01 | Env Config | Refresh interval configurable | Change `REFRESH_INTERVAL` env var | Server uses new value on restart | |
| M4-F3-TC02 | Env Config | Company list configurable | Change `COMPANIES` env var | Only specified companies are scraped | |

---

## 2. API Test Cases

### Endpoint: `GET /api/announcements`

| TC ID | Scenario | Method | Headers | Expected Status | Expected Body | Notes |
|-------|----------|--------|---------|-----------------|---------------|-------|
| API-TC01 | Normal successful fetch | GET | `Accept: application/json` | 200 | Array of 12 announcement objects | Happy path |
| API-TC02 | Correct data shape | GET | — | 200 | Each object has `company`, `date`, `title`, `url` | Schema validation |
| API-TC03 | Companies present | GET | — | 200 | `company` values include `Infosys`, `HCL`, `Reliance`, `TCS` | |
| API-TC04 | Announcement count | GET | — | 200 | Exactly 3 entries per company (12 total) | |
| API-TC05 | Content-Type header | GET | — | 200 | `Content-Type: application/json` in response | |
| API-TC06 | Invalid method — POST | POST | — | 405 | Method Not Allowed | |
| API-TC07 | Invalid method — DELETE | DELETE | — | 405 | Method Not Allowed | |
| API-TC08 | Dates sorted descending | GET | — | 200 | Announcements within each company ordered newest first | |
| API-TC09 | Cache header present | GET | — | 200 | `Cache-Control` or `Last-Modified` header present | Optional but good practice |
| API-TC10 | Concurrent requests | GET ×10 parallel | — | 200 (all) | All requests return valid data, no race condition | |
| API-TC11 | Scraper unavailable (cold cache) | GET (Screener down, no cache) | — | 503 or 200 with empty/error body | Graceful degradation message | |
| API-TC12 | Scraper unavailable (warm cache) | GET (Screener down, cache populated) | — | 200 | Last known data returned | |
| API-TC13 | Response time | GET | — | 200 | Response within 2000 ms (cache hit) | Performance baseline |

---

## 3. Edge Cases

### Data Layer Edge Cases

| EC ID | Area | Scenario | Expected Behavior |
|-------|------|----------|-------------------|
| EC-DL-01 | Scraper | Screener.in returns HTTP 429 (rate limited) | Retry with backoff; log warning; serve cache |
| EC-DL-02 | Scraper | Screener.in returns HTTP 503 | Fallback to cache; no crash |
| EC-DL-03 | Scraper | Network timeout (>30s) | Request aborted; error logged; cache served |
| EC-DL-04 | Parser | HTML structure changes (Screener redesign) | Parser returns empty/null gracefully; error flagged |
| EC-DL-05 | Parser | Announcement text contains special characters (`&amp;`, `<`, `>`) | Text decoded correctly, no raw HTML entities shown |
| EC-DL-06 | Parser | Date in unexpected format | Date stored as raw string; no crash |
| EC-DL-07 | Parser | Announcement with empty title | Entry skipped or placeholder shown |
| EC-DL-08 | Filter | Company has 0 announcements | Empty array returned for that company; no crash |
| EC-DL-09 | Filter | Duplicate announcement entries in source | Deduplication or first occurrence kept |
| EC-DL-10 | Data Model | URL contains query params or fragments | Full URL preserved as-is |

### Backend Edge Cases

| EC ID | Area | Scenario | Expected Behavior |
|-------|------|----------|-------------------|
| EC-BE-01 | Cache | Server restarts mid-scrape | Next scheduled scrape repopulates cache cleanly |
| EC-BE-02 | Cache | Cache is stale by > 2 hours | Data served with stale warning or force-refresh triggered |
| EC-BE-03 | Scheduler | Refresh task throws unhandled exception | Exception caught; scheduler continues; next run not skipped |
| EC-BE-04 | Scheduler | Two refresh tasks overlap (slow scrape + next interval) | Second task queued or skipped to prevent double scrape |
| EC-BE-05 | API | Extremely large announcement text | Truncated at reasonable limit (e.g., 500 chars) or full text served |
| EC-BE-06 | Env Config | `REFRESH_INTERVAL` set to 0 or negative | Default interval used; warning logged |
| EC-BE-07 | Env Config | Invalid company name in `COMPANIES` list | Invalid entry skipped; valid companies still scraped |

### Frontend Edge Cases

| EC ID | Area | Scenario | Expected Behavior |
|-------|------|----------|-------------------|
| EC-FE-01 | API call | Backend unreachable from browser | Error message shown in UI; no blank screen |
| EC-FE-02 | Data | Company returns 0 announcements | Section shows "No announcements available" |
| EC-FE-03 | Data | Very long announcement text | Text wraps or truncates with ellipsis; no layout break |
| EC-FE-04 | Data | Announcement date is null/missing | "Date unavailable" or blank; no JS error |
| EC-FE-05 | Rendering | API returns unexpected JSON shape | UI renders partial data or shows error gracefully |
| EC-FE-06 | Rendering | Browser has JS disabled | Page still loads (if server-side rendered) or shows fallback message |
| EC-FE-07 | Responsive | Very narrow viewport (< 320px) | No horizontal overflow; content still readable |

---

## 4. UAT Checklist

### Pre-UAT Setup
- [ ] App deployed and accessible at Railway public URL
- [ ] All 4 companies (Infosys, HCL, Reliance, TCS) confirmed in configuration
- [ ] Tester has access to both desktop and mobile browser
- [ ] Reference design (`SampleScreen.png`) available for visual comparison

---

### UAT-01: Data Accuracy
- [ ] Dashboard shows announcements for **Infosys**
- [ ] Dashboard shows announcements for **HCL**
- [ ] Dashboard shows announcements for **Reliance**
- [ ] Dashboard shows announcements for **TCS**
- [ ] Each company shows **exactly 3** announcements
- [ ] Announcements match what is currently visible on Screener.in (spot-check 2 companies)
- [ ] Dates are correct and formatted consistently
- [ ] Announcement text is readable and free of HTML artifacts

---

### UAT-02: UI / Visual Design
- [ ] Layout matches `SampleScreen.png` overall structure
- [ ] Company names clearly labeled/grouped
- [ ] Date displayed **before** announcement text in each entry
- [ ] Color scheme matches the design reference
- [ ] Font and text sizes match the design reference
- [ ] No overlapping or misaligned elements on desktop (1280×800)
- [ ] Page loads without visible errors or broken elements

---

### UAT-03: Responsiveness
- [ ] App is usable on desktop Chrome (latest)
- [ ] App is usable on desktop Edge/Firefox
- [ ] App is usable on mobile Chrome (Android or iOS simulation)
- [ ] No horizontal scrollbar on desktop viewport
- [ ] Content readable on 375px-wide mobile viewport

---

### UAT-04: Performance & Reliability
- [ ] Page loads within **3 seconds** on a standard connection
- [ ] API `/api/announcements` responds within **2 seconds**
- [ ] Refreshing the page does not cause errors or blank content
- [ ] App continues to display data after leaving tab open for 30+ minutes (cache refresh works)

---

### UAT-05: Error & Edge Condition Acceptance
- [ ] If one company's data is unavailable, the other 3 still display (no full crash)
- [ ] A clear message is shown if all data is unavailable (not a blank or broken page)
- [ ] No raw error stack traces or technical messages visible to end user

---

### UAT-06: Deployment Acceptance
- [ ] App accessible from the Railway public URL without VPN or special configuration
- [ ] HTTPS enabled on Railway domain
- [ ] App survives a Railway service restart (data reloads on startup)
- [ ] Environment variables are not exposed in frontend source or API responses

---

### UAT Sign-Off

| Area | Tester | Date | Status |
|------|--------|------|--------|
| Data Accuracy | | | |
| UI / Visual Design | | | |
| Responsiveness | | | |
| Performance | | | |
| Error Handling | | | |
| Deployment | | | |

**Overall UAT Decision:** `[ ] Pass` &nbsp; `[ ] Pass with minor issues` &nbsp; `[ ] Fail — rework required`

**Notes / Defects Found:**

---
