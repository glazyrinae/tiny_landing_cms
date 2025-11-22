from django.db import models
from django.utils.text import slugify

class HeroSection(models.Model):
    title = models.CharField(max_length=200, blank=False, verbose_name="Заголовок блока")
    desc = models.CharField(max_length=200, blank=False,  verbose_name="Описание блока")
    slug = models.SlugField(max_length=250, verbose_name="Ссылка на блок")
    is_active = models.BooleanField(default=True, verbose_name="Видимость")
    background = models.ImageField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'section_hero_main' 
        verbose_name = "Блок заглавный"
        verbose_name_plural = "Блок заглавный"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class HeroSectionMarkers(models.Model):
    title = models.CharField(max_length=100, blank=True,  verbose_name="Доп.информация")
    icon = models.CharField(max_length=100, blank=True,  verbose_name="названия иконки")
    is_active = models.BooleanField(default=True, verbose_name="Видимость")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    section = models.ForeignKey(HeroSection, on_delete=models.CASCADE, related_name="markers", verbose_name="Связанный блок")
    
    class Meta:
        db_table = 'section_hero_markers'