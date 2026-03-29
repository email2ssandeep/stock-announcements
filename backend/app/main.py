import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.database import init_db, SessionLocal
from app.core.seed import seed_companies
from app.services import scheduler_service, announcement_service
from app.controllers import announcement_controller, health_controller

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

STATIC_DIR = Path(__file__).parent.parent / "static"


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()
    db = SessionLocal()
    try:
        seed_companies(db)
        announcement_service.refresh_announcements(db)
    finally:
        db.close()

    def scheduled_refresh():
        db = SessionLocal()
        try:
            announcement_service.refresh_announcements(db)
        finally:
            db.close()

    scheduler_service.start(scheduled_refresh)
    yield
    # Shutdown
    scheduler_service.stop()


app = FastAPI(title="Stock Announcements", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(announcement_controller.router)
app.include_router(health_controller.router)

# Serve React frontend (production build)
if STATIC_DIR.exists():
    app.mount("/assets", StaticFiles(directory=STATIC_DIR / "assets"), name="assets")

    @app.get("/{full_path:path}", include_in_schema=False)
    def serve_spa(full_path: str):
        index = STATIC_DIR / "index.html"
        return FileResponse(str(index))
