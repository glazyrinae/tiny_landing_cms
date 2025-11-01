import logging


from django.contrib import admin
from django.utils.html import format_html
from .models import AboutSection, AboutSectionWidget, AboutSectionImages, AboutSectionFeatures

logger = logging.getLogger("about")

# Constants
THUMBNAIL_SIZE = (350, 200)

class ImageInline(admin.StackedInline):
    model = AboutSectionImages
    extra = 0
    readonly_fields = ("thumbnail_preview",)
    fields = ("src", "alt", "thumbnail_preview")

    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html(
                f'<img src="{obj.thumbnail.url}" width="{THUMBNAIL_SIZE[0]}" height="{THUMBNAIL_SIZE[1]}" />'
            )
        return "-"

class AboutSectionFeaturesInline(admin.StackedInline):
    model = AboutSectionFeatures
    extra = 0
    fields = ("title", "css_class", 'is_active')


@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    inlines = [ImageInline, AboutSectionFeaturesInline]

@admin.register(AboutSectionWidget)
class AboutSectionWidgetAdmin(admin.ModelAdmin):
    list_display = ('html_content', 'is_active')
