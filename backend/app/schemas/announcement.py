from pydantic import BaseModel


class AnnouncementOut(BaseModel):
    date: str
    title: str
    source_url: str | None = None

    model_config = {"from_attributes": True}


class AllAnnouncementsOut(BaseModel):
    infosys: list[AnnouncementOut] = []
    hcl: list[AnnouncementOut] = []
    reliance: list[AnnouncementOut] = []
    tcs: list[AnnouncementOut] = []
