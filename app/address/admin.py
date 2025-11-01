import logging


from django.contrib import admin
from django.utils.html import format_html
from .models import AddressSection, AddressSectionFeatures

logger = logging.getLogger("about")

class AddressSectionFeaturesInline(admin.StackedInline):
    model = AddressSectionFeatures
    extra = 0
    fields = ("url", 'icon')


@admin.register(AddressSection)
class AddressSectionAdmin(admin.ModelAdmin):
    list_display = ('address', 'phone', 'hours_work', 'slug', 'geo_tag')
    inlines = [AddressSectionFeaturesInline]
