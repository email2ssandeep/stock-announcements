from sqlalchemy.orm import Session
from app.models.announcement import Announcement
from app.repositories.base import BaseRepository


class AnnouncementRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(Announcement, db)

    def get_by_company(self, company_id: int) -> list[Announcement]:
        return (
            self.db.query(Announcement)
            .filter(Announcement.company_id == company_id)
            .order_by(Announcement.rank)
            .all()
        )

    def replace_for_company(self, company_id: int, new_announcements: list[Announcement]):
        self.db.query(Announcement).filter(Announcement.company_id == company_id).delete()
        for ann in new_announcements:
            self.db.add(ann)
        self.db.commit()
