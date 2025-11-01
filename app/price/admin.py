import logging
from django.contrib import admin
from django.utils.html import format_html
from .models import PriceSection, PriceSectionFeatures

logger = logging.getLogger("price")


# Inline для тарифов внутри секции
class PriceSectionFeaturesInline(admin.StackedInline):
    model = PriceSectionFeatures
    extra = 0
    fields = ("title", "price", 'is_recommended', 'services', 'period', 'is_active')
    verbose_name = "Тариф"
    verbose_name_plural = "Тарифы"

@admin.register(PriceSection)
class PriceSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'desc', 'slug', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'desc')
    inlines = [PriceSectionFeaturesInline]  # Только features inline