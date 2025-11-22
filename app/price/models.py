from django.db import models
from django.utils.text import slugify

class PriceSection(models.Model):
    title = models.CharField(max_length=200, blank=False, verbose_name="Заголовок блока")
    desc = models.CharField(max_length=800, blank=False,  verbose_name="Описание блока")
    slug = models.SlugField(max_length=250, verbose_name="Ссылка на блок")
    is_active = models.BooleanField(default=True, verbose_name="Видимость")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'section_price_main' 
        verbose_name = "Цены и услуги"
        verbose_name_plural = "Цены и услуги"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class PriceSectionFeatures(models.Model):
    title = models.CharField(max_length=100, blank=True,  verbose_name="Описание")
    price = models.CharField(max_length=100, blank=True,  verbose_name="Цена")
    period = models.CharField(max_length=20, blank=True,  verbose_name="Период")
    is_recommended = models.BooleanField(default=True, verbose_name="Рекомендуемый")
    is_active = models.BooleanField(default=True, verbose_name="Видимость")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    section = models.ForeignKey(PriceSection, on_delete=models.CASCADE, related_name="features")
    services = models.TextField(max_length=10000, blank=True, verbose_name="Список услуг")
    class Meta:
        db_table = 'section_price_features'