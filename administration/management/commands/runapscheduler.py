from django.conf import settings
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from jobs import jobs


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options) -> None:
        scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            jobs.update_stocks,
            trigger=CronTrigger(hour=settings.HOUR_UPDATE_LC_STOCKS,
                                minute=settings.MINUTES_UPDATE_LC_STOCKS,
                                ),
            id='update_stocks',
            max_instances=1,
            replace_existing=True,
        )

        scheduler.add_job(
            jobs.update_fiis,
            trigger=CronTrigger(hour=settings.HOUR_UPDATE_LC_FIIS,
                                minute=settings.MINUTES_UPDATE_LC_FIIS,
                                ),
            id='update_fiis',
            max_instances=1,
            replace_existing=True,
        )

        scheduler.start()
