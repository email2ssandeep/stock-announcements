from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.announcement import AllAnnouncementsOut, AnnouncementOut
from app.services import announcement_service

router = APIRouter(prefix="/api", tags=["announcements"])


@router.get("/announcements", response_model=AllAnnouncementsOut)
def get_all_announcements(db: Session = Depends(get_db)):
    data = announcement_service.get_all_announcements(db)
    return AllAnnouncementsOut(**data)


@router.get("/announcements/{ticker}", response_model=list[AnnouncementOut])
def get_company_announcements(ticker: str, db: Session = Depends(get_db)):
    ticker = ticker.lower()
    data = announcement_service.get_announcements_for_company(ticker, db)
    if data is None:
        raise HTTPException(status_code=404, detail=f"Company '{ticker}' not found")
    return data
