I need your permission to write to `Docs\brd.md`. Please approve the write access, or let me know if you'd prefer I just display the BRD here.

In the meantime, here's the full BRD:

---

# Business Requirements Document (BRD)
## Stock Announcement Alerts — Web Application

**Client:** Michael | **Developer:** Sandeep | **Date:** 2026-03-29 | **Version:** 1.0

---

## 1. Scope

This project delivers a web-based application that monitors and displays the latest corporate announcements for a defined set of NSE/BSE-listed companies. The application fetches announcement data from Screener.in, presents it through a dashboard UI, and is deployed on Railway. A future mobile app conversion will also be evaluated.

**In Scope:**
- Announcement monitoring for 4 companies: Infosys, HCL, Reliance, and TCS
- Web-based dashboard with an announcement alerts section
- Data sourced from Screener.in company pages
- Deployment to Railway cloud platform
- Feasibility assessment for mobile app conversion

**Out of Scope:**
- Real-time or historical share price data
- Email or push notification delivery
- Any companies beyond the four listed above
- Trading or portfolio management functionality

---

## 2. Features

**F1 — Announcement Dashboard**
- A dedicated Announcement Alert Section on the UI displaying the latest announcements for all four monitored companies.
- Each announcement entry must display the announcement date at the start of the entry.
- The UI must match the visual style provided in `SampleScreen.png`.

**F2 — Announcement Data Feed**
- Retrieve announcement data from Screener.in company pages for each of the four tracked companies.
- Display only the latest 3 announcements per company at any given time.

**F3 — Deployment**
- Deploy and host the application on Railway, publicly accessible via a Railway-provided URL.

**F4 — Mobile App Conversion (Future)**
- Evaluate feasibility of converting the web application into a mobile app. Secondary objective; does not block initial release.

---

## 3. Business Rules

| # | Rule |
|---|------|
| BR-01 | Only announcements from Infosys, HCL, Reliance, and TCS are monitored. No other companies. |
| BR-02 | A maximum of 3 announcements per company shall be displayed; older entries beyond this limit are not shown. |
| BR-03 | Each announcement entry must begin with its announcement date. |
| BR-04 | Share price data must not be displayed anywhere in the application. |
| BR-05 | Announcement data must be sourced exclusively from Screener.in. No other data sources are permitted. |
| BR-06 | The production deployment platform is Railway. No other hosting provider is to be used for production. |

---

## 4. Assumptions

| # | Assumption |
|---|------------|
| A-01 | Screener.in's announcement section for each company is publicly accessible without authentication or a paid subscription. |
| A-02 | The structure of Screener.in company pages remains stable and does not change frequently. |
| A-03 | The UI design must closely follow the style shown in `SampleScreen.png`, treated as the authoritative design reference. |
| A-04 | "Latest 3 announcements" refers to the 3 most recently dated entries on Screener.in, not filtered by any other criteria. |
| A-05 | The four company names map directly to their respective Screener.in profile pages. |
| A-06 | Mobile app conversion is a post-launch consideration with no committed timeline or budget at this stage. |
| A-07 | Railway's free or starter tier is sufficient for expected traffic during initial rollout. |
| A-08 | No user authentication or login is required to access the dashboard. |

---

*Prepared by Sandeep based on requirements discussion with Michael.*
