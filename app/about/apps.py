from django.apps import AppConfig  # type: ignore


class AboutConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "about"

    def ready(self):
        # Импортируем сигналы
        import about.signals
