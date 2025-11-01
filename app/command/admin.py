import logging

from django.contrib import admin
from django.utils.html import format_html
from .models import CommandSection, CommandSectionFeatures
logger = logging.getLogger("command")

# Constants
THUMBNAIL_SIZE = (350, 200)

class ImageInline(admin.StackedInline):
    model = CommandSectionFeatures
    extra = 0
    readonly_fields = ("thumbnail_preview",)
    fields = ("title", "desc", 'name' , 'status','social', 'is_active', "src", "alt", "thumbnail_preview")

    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html(
                f'<img src="{obj.thumbnail.url}" width="{THUMBNAIL_SIZE[0]}" height="{THUMBNAIL_SIZE[1]}" />'
            )
        return "-"

@admin.register(CommandSection)
class CommandSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'desc', 'slug', 'is_active', 'created_at')
    inlines = [ImageInline]

