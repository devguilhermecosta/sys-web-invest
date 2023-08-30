from django.conf import settings
from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import update

scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)


def start() -> None:
    scheduler.add_job(
        update,
        'cron',
        hour=23,
        minute=40,
        )

    scheduler.start()
