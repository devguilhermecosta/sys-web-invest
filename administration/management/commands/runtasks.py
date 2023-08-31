from django.core.management.base import BaseCommand
from jobs import jobs


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options) -> None:
        jobs.update_stocks()
        jobs.update_fiis()
