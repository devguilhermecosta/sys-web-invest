from django.apps import AppConfig


class DashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dashboard'

    def ready(self) -> None:
        from jobs import updater
        import os

        if os.environ.get('RUN_MAIN'):
            updater.start()
