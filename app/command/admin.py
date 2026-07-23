import logging

from django.contrib import admin
from tiny_cms.admin_utils import ADMIN_IMAGE_PREVIEW_CSS, admin_image_preview
from .models import CommandSection, CommandSectionFeatures
logger = logging.getLogger("command")

class ImageInline(admin.StackedInline):
    model = CommandSectionFeatures
    extra = 0
    readonly_fields = ("thumbnail_preview",)
    fields = ("title", "desc", 'name' , 'status','social', 'is_active', "src", "alt", "thumbnail_preview")

    def thumbnail_preview(self, obj):
        return admin_image_preview(
            getattr(obj, "thumbnail", None),
            getattr(obj, "alt", ""),
        )

    class Media:
        css = {"all": (ADMIN_IMAGE_PREVIEW_CSS,)}

@admin.register(CommandSection)
class CommandSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'desc', 'slug', 'is_active', 'created_at')
    inlines = [ImageInline]
