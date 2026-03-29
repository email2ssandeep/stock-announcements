from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Announcement(Base):
    __tablename__ = "announcements"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    title = Column(String, nullable=False)
    announcement_date = Column(String, nullable=False)   # stored as normalized string
    source_url = Column(String, nullable=True)
    scraped_at = Column(DateTime, nullable=False)
    rank = Column(Integer, nullable=False)               # 1 = most recent, up to 3

    company = relationship("Company", back_populates="announcements")
