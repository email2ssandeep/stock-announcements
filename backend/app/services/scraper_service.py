import logging
import re
import httpx
from bs4 import BeautifulSoup
from app.config import COMPANY_URLS

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    )
}
TIMEOUT = 15  # seconds
MAX_ANNOUNCEMENTS = 3


def _parse_announcements(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")

    # Screener.in announcements are inside #documents or #announcements section
    section = soup.find("section", id="documents") or soup.find("section", id="announcements")
    if not section:
        logger.warning("Announcements section not found in page HTML")
        return []

    results = []
    rows = section.select("ul.list-links li") or section.select("div.announcement-row")

    # Date pattern at start of div text: "25 Mar - ...", "2d - ..."
    DATE_RE = re.compile(
        r"^(\d{1,2}\s+\w{3}(?:\s+\d{4})?|\d+[dh])\s*-\s*", re.IGNORECASE
    )

    for row in rows[:MAX_ANNOUNCEMENTS]:
        anchor = row.find("a")
        href = anchor.get("href", "") if anchor else ""
        if href and not href.startswith("http"):
            href = "https://www.screener.in" + href

        # Screener.in structure:
        #   <a> Announcement Type <div class="ink-600 smaller">DATE - description</div> </a>
        subtitle_div = row.find("div", class_="ink-600")
        if subtitle_div:
            subtitle_text = subtitle_div.get_text(strip=True)
            m = DATE_RE.match(subtitle_text)
            date_str = m.group(1) if m else "N/A"
            description = subtitle_text[m.end():].strip() if m else subtitle_text

            # Main title: anchor text node excluding the div
            subtitle_div.extract()
            main_title = anchor.get_text(strip=True) if anchor else ""
            title = f"{main_title} — {description}" if description else main_title
        else:
            # Fallback: use full anchor text
            title = anchor.get_text(strip=True) if anchor else row.get_text(strip=True)
            date_str = "N/A"

        if title:
            results.append({
                "title": title,
                "date": date_str,
                "source_url": href,
            })

    return results


def scrape_company(ticker: str) -> list[dict]:
    url = COMPANY_URLS.get(ticker)
    if not url:
        logger.error("Unknown ticker: %s", ticker)
        return []

    try:
        with httpx.Client(headers=HEADERS, timeout=TIMEOUT, follow_redirects=True) as client:
            response = client.get(url)
            response.raise_for_status()
        return _parse_announcements(response.text)
    except httpx.TimeoutException:
        logger.warning("Timeout scraping %s (%s)", ticker, url)
    except httpx.HTTPStatusError as e:
        logger.warning("HTTP %s for %s", e.response.status_code, url)
    except Exception as e:
        logger.exception("Unexpected error scraping %s: %s", ticker, e)

    return []


def scrape_all() -> dict[str, list[dict]]:
    return {ticker: scrape_company(ticker) for ticker in COMPANY_URLS}
