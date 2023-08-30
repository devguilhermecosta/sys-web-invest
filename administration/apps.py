from django.apps import AppConfig


class AdministrationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'administration'

    def ready(self) -> None:
        from jobs import updater
        import os

        if os.environ.get('RUN_MAIN'):
            updater.start()
