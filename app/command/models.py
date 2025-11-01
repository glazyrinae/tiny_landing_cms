from django.db import models
from django.utils.text import slugify

class CommandSection(models.Model):
    title = models.CharField(max_length=200, blank=False, verbose_name="Заголовок блока")
    desc = models.TextField(max_length=800, blank=False,  verbose_name="Описание блока")
    slug = models.SlugField(max_length=250, verbose_name="Ссылка на блок")
    is_active = models.BooleanField(default=True, verbose_name="Видимость")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'section_command_main' 
        verbose_name = "Наша команда"
        verbose_name_plural = "Наша команда"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class CommandSectionFeatures(models.Model):
    title = models.CharField(max_length=100, blank=True,  verbose_name="Доп.информация")
    name = models.CharField(max_length=100, blank=True,  verbose_name="имя")
    status = models.CharField(max_length=100, blank=True,  verbose_name="должность")
    desc = models.CharField(max_length=100, blank=True,  verbose_name="описание")
    social = models.CharField(max_length=100, blank=True,  verbose_name="контакты")
    is_active = models.BooleanField(default=True, verbose_name="Видимость")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    section = models.ForeignKey(CommandSection, on_delete=models.CASCADE, related_name="features")
    src = models.ImageField(blank=True)
    thumbnail = models.ImageField(upload_to="%Y/%m/%d/thumbnails", blank=True, null=True)
    alt = models.CharField(max_length=100, blank=True,  verbose_name="Описание картинки")

    class Meta:
        db_table = 'section_command_features'