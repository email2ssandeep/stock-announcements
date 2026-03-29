import logging
from apscheduler.schedulers.background import BackgroundScheduler
from app.config import SCHEDULER_INTERVAL_MINUTES

logger = logging.getLogger(__name__)
_scheduler = BackgroundScheduler()


def start(refresh_fn):
    _scheduler.add_job(
        refresh_fn,
        trigger="interval",
        minutes=SCHEDULER_INTERVAL_MINUTES,
        id="refresh_announcements",
        replace_existing=True,
    )
    _scheduler.start()
    logger.info("Scheduler started — refresh every %d min", SCHEDULER_INTERVAL_MINUTES)


def stop():
    if _scheduler.running:
        _scheduler.shutdown(wait=False)
        logger.info("Scheduler stopped")
