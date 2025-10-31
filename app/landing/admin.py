import logging

from django import forms
from django.contrib import admin
from django.utils.html import format_html
from .models import Page, BlockType, Block, Images

logger = logging.getLogger("landing")

# Constants
THUMBNAIL_SIZE = (350, 200)
TEXT_ROWS = 20
FONT_SIZE = 16

class ImageInline(admin.StackedInline):
    model = Images
    extra = 0
    readonly_fields = ("thumbnail_preview",)
    fields = ("image", "thumbnail_preview", "image_type")

    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html(
                f'<img src="{obj.thumbnail.url}" width="{THUMBNAIL_SIZE[0]}" height="{THUMBNAIL_SIZE[1]}" />'
            )
        return "-"


class BlockInline(admin.TabularInline):
    model = Block
    extra = 1
    fields = ('block_type', 'title', 'order', 'is_active')
    ordering = ('order',)

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [BlockInline]

@admin.register(BlockType)
class BlockTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'template', 'description')
    search_fields = ('name', 'template')

@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ('page', 'block_type', 'title', 'order', 'is_active')
    list_filter = ('block_type', 'is_active', 'page')
    search_fields = ('title', 'content')
    list_editable = ('order', 'is_active')
    ordering = ('page', 'order')
