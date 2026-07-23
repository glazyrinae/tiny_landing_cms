import logging


from django.contrib import admin
from tiny_cms.admin_utils import ADMIN_IMAGE_PREVIEW_CSS, admin_image_preview
from .models import AboutSection, AboutSectionWidget, AboutSectionImages, AboutSectionFeatures

logger = logging.getLogger("about")

class ImageInline(admin.StackedInline):
    model = AboutSectionImages
    extra = 0
    readonly_fields = ("thumbnail_preview",)
    fields = ("src", "alt", "thumbnail_preview")

    def thumbnail_preview(self, obj):
        return admin_image_preview(
            getattr(obj, "thumbnail", None),
            getattr(obj, "alt", ""),
        )

    class Media:
        css = {"all": (ADMIN_IMAGE_PREVIEW_CSS,)}

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
