from sqlalchemy.orm import Session
from app.models.company import Company
from app.config import COMPANY_URLS

SEED_COMPANIES = [
    {"ticker": "infosys",  "name": "Infosys",  "screener_url": COMPANY_URLS["infosys"]},
    {"ticker": "hcl",      "name": "HCL",      "screener_url": COMPANY_URLS["hcl"]},
    {"ticker": "reliance", "name": "Reliance", "screener_url": COMPANY_URLS["reliance"]},
    {"ticker": "tcs",      "name": "TCS",      "screener_url": COMPANY_URLS["tcs"]},
]


def seed_companies(db: Session):
    for data in SEED_COMPANIES:
        exists = db.query(Company).filter(Company.ticker == data["ticker"]).first()
        if not exists:
            db.add(Company(**data))
    db.commit()
