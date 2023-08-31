from django.conf import settings
from apscheduler.schedulers.background import BackgroundScheduler
from jobs import jobs


scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)

scheduler.add_job(
    jobs.update_stocks,
    'cron',
    hour=settings.HOUR_UPDATE_LC_STOCKS,
    minute=settings.MINUTES_UPDATE_LC_STOCKS,
)

scheduler.add_job(
    jobs.update_fiis,
    'cron',
    hour=settings.HOUR_UPDATE_LC_FIIS,
    minute=settings.MINUTES_UPDATE_LC_FIIS,
)

scheduler.start()
