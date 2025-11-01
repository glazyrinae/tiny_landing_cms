from django.apps import AppConfig  # type: ignore


class ServiceConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "service"
