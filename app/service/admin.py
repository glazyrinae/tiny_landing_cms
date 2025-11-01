import logging


from django.contrib import admin
from django.utils.html import format_html
from .models import ServiceSection, ServiceSectionFeatures

logger = logging.getLogger("about")

class ServiceSectionFeaturesInline(admin.StackedInline):
    model = ServiceSectionFeatures
    extra = 0
    fields = ("title", "desc", 'icon', 'is_active')


@admin.register(ServiceSection)
class ServiceSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    inlines = [ServiceSectionFeaturesInline]
