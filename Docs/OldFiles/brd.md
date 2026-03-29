I'll proceed with the BRD based on the conversation. The screenshot reference will be noted as a UI reference artifact.

---

# Business Requirements Document (BRD)
## Stock Announcement Alerts — Web Application

**Client:** Michael
**Developer:** Sandeep
**Date:** 2026-03-27
**Version:** 1.0

---

## 1. Scope

This project delivers a web-based application that monitors and displays the latest corporate announcements for a defined set of NSE/BSE-listed companies. The application will fetch announcement data from Screener.in, present it through a dashboard UI, and be deployed on Railway. A future mobile app conversion will also be evaluated.

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

### F1 — Announcement Dashboard
- A dedicated **Announcement Alert Section** on the UI displaying the latest announcements for all four monitored companies.
- Each announcement entry must display the **announcement date** at the start of the entry.
- The UI must match the visual style provided in the sample screenshot (`SampleScreen.png`).

### F2 — Announcement Data Feed
- The application must scrape or retrieve announcement data from **Screener.in** company pages for each of the four tracked companies.
- Only the **latest 3 announcements per company** are to be displayed at any given time.

### F3 — Deployment
- The application must be deployed and hosted on **Railway**.
- The app must be publicly accessible via a Railway-provided URL.

### F4 — Mobile App Conversion (Future)
- Evaluate the feasibility of converting the web application into a mobile app.
- This is a secondary objective and does not block the initial release.

---

## 3. Business Rules

| # | Rule |
|---|------|
| BR-01 | Only announcements from **Infosys, HCL, Reliance, and TCS** are monitored. No other companies. |
| BR-02 | A maximum of **3 announcements per company** shall be displayed; older announcements beyond this limit are not shown. |
| BR-03 | Each announcement entry **must begin with its announcement date**. |
| BR-04 | **Share price data must not be displayed** anywhere in the application. |
| BR-05 | Announcement data must be sourced **exclusively from Screener.in**. No other data sources are permitted. |
| BR-06 | The production deployment platform is **Railway**. No other hosting provider is to be used for production. |

---

## 4. Assumptions

| # | Assumption |
|---|------------|
| A-01 | Screener.in's announcement section for each company is publicly accessible without authentication or a paid subscription. |
| A-02 | The structure of Screener.in company pages (announcement section HTML/layout) remains stable and does not change frequently. |
| A-03 | The UI design must closely follow the style shown in `D:\Sandeep_AITest\Test_Claude\Source\StockAlerts\SampleScreen.png`. This file is treated as the authoritative design reference. |
| A-04 | "Latest 3 announcements" refers to the 3 most recently dated announcements as listed on Screener.in, not filtered by any other criteria. |
| A-05 | The four company names (Infosys, HCL, Reliance, TCS) map directly to their respective Screener.in profile pages. |
| A-06 | Mobile app conversion is a post-launch consideration and does not have a committed timeline or additional budget attached at this stage. |
| A-07 | Railway's free or starter tier is sufficient for the expected traffic volume during initial rollout. |
| A-08 | No user authentication or login is required to access the dashboard. |

---

*Document prepared by Sandeep based on requirements discussion with Michael.*
