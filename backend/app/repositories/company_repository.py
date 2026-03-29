from sqlalchemy.orm import Session
from app.models.company import Company
from app.repositories.base import BaseRepository


class CompanyRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(Company, db)

    def get_by_ticker(self, ticker: str) -> Company | None:
        return self.db.query(Company).filter(Company.ticker == ticker).first()

    def exists(self, ticker: str) -> bool:
        return self.get_by_ticker(ticker) is not None
