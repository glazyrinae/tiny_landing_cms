from django.apps import AppConfig  # type: ignore


class CommandConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "command"

    def ready(self):
        # Импортируем сигналы
        import command.signals
