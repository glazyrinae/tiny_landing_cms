from django.db import models
from django.utils.text import slugify

class AddressSection(models.Model):
    address = models.CharField(max_length=200, blank=False, verbose_name="адрес")
    phone = models.CharField(max_length=800, blank=False,  verbose_name="телефон")
    hours_work = models.CharField(max_length=800, blank=False,  verbose_name="режим работы")
    slug = models.SlugField(max_length=250, verbose_name="Ссылка на блок")
    geo_tag = models.CharField(max_length=1200, verbose_name="Гео тэг для карты")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'section_address_main' 
        verbose_name = "Адресный блок"
        verbose_name_plural = "Адресный блок"

    def __str__(self):
        return self.address

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.address)
        super().save(*args, **kwargs)

class AddressSectionFeatures(models.Model):
    url = models.CharField(max_length=100, blank=True,  verbose_name="Cсылка")
    icon = models.CharField(max_length=100, blank=True,  verbose_name="icon")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    section = models.ForeignKey(AddressSection, on_delete=models.CASCADE, related_name="features")
    
    class Meta:
        db_table = 'section_address_features'