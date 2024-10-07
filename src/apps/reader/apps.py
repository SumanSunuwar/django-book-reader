from django.apps import AppConfig


class ReaderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.reader'

    def ready(self):
            import apps.reader.signals