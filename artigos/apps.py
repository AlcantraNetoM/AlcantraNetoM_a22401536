from django.apps import AppConfig


class ArtigosConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "artigos"

    def ready(self):
        from . import signals  # noqa: F401
