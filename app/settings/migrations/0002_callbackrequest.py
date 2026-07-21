# Generated manually for callback submissions.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("settings", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="CallbackRequest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=120, verbose_name="Имя")),
                ("phone", models.CharField(max_length=32, verbose_name="Телефон")),
                ("message", models.TextField(blank=True, verbose_name="Сообщение")),
                (
                    "is_processed",
                    models.BooleanField(default=False, verbose_name="Обработано"),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Создано"),
                ),
            ],
            options={
                "verbose_name": "Заявка",
                "verbose_name_plural": "Заявки",
                "ordering": ["-created_at"],
            },
        ),
    ]
