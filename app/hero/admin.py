import logging


from django.contrib import admin
from django.utils.html import format_html
from .models import HeroSection, HeroSectionMarkers

logger = logging.getLogger("hero")


class HeroSectionMarkersAdmin(admin.StackedInline):
    model = HeroSectionMarkers
    extra = 0
    fields = ("title", "icon", 'is_active')


@admin.register(HeroSection)
class AboutSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'desc', 'is_active', 'background', 'created_at')
    inlines = [HeroSectionMarkersAdmin]
