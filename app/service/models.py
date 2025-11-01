from django.db import models
from django.utils.text import slugify

class ServiceSection(models.Model):
    title = models.CharField(max_length=200, blank=False, verbose_name="Заголовок блока")
    desc = models.CharField(max_length=800, blank=False,  verbose_name="Описание блока")
    slug = models.SlugField(max_length=250, verbose_name="Ссылка на блок")
    is_active = models.BooleanField(default=True, verbose_name="Видимость")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'section_service_main' 
        verbose_name = "Блок услуг"
        verbose_name_plural = "Блок услуг"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class ServiceSectionFeatures(models.Model):
    title = models.CharField(max_length=100, blank=True,  verbose_name="Доп.информация")
    desc = models.CharField(max_length=100, blank=True,  verbose_name="Oписание")
    icon = models.CharField(max_length=100, blank=True,  verbose_name="icon")
    is_active = models.BooleanField(default=True, verbose_name="Видимость")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    section = models.ForeignKey(ServiceSection, on_delete=models.CASCADE, related_name="features")
    
    class Meta:
        db_table = 'section_service_features'