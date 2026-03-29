import os
from dotenv import load_dotenv

load_dotenv()

ADMIN_KEY: str = os.getenv("ADMIN_KEY", "changeme")
CACHE_TTL_SECONDS: int = int(os.getenv("CACHE_TTL_SECONDS", 1800))   # 30 min
SCHEDULER_INTERVAL_MINUTES: int = int(os.getenv("SCHEDULER_INTERVAL_MINUTES", 30))
DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./announcements.db")

COMPANY_URLS: dict = {
    "infosys":  "https://www.screener.in/company/INFY/",
    "hcl":      "https://www.screener.in/company/HCLTECH/",
    "reliance": "https://www.screener.in/company/RELIANCE/",
    "tcs":      "https://www.screener.in/company/TCS/",
}
