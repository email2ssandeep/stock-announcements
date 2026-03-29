from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, unique=True, nullable=False)   # e.g. "infosys"
    name = Column(String, nullable=False)                  # e.g. "Infosys"
    screener_url = Column(String, nullable=False)

    announcements = relationship("Announcement", back_populates="company", cascade="all, delete-orphan")
