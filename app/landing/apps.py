from django.apps import AppConfig  # type: ignore


class LandingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "landing"

    def ready(self):
        # Импортируем сигналы
        import landing.signals
