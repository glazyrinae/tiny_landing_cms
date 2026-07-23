from django.utils.html import format_html


ADMIN_IMAGE_PREVIEW_SIZE = (350, 200)
ADMIN_IMAGE_PREVIEW_CSS = "css/admin-image-preview.css"


def admin_image_preview(image, alt="", size=ADMIN_IMAGE_PREVIEW_SIZE):
    if not image:
        return "-"

    width, height = size
    return format_html(
        '<div class="admin-image-preview" style="--preview-width: {}px; --preview-height: {}px;">'
        '<img src="{}" alt="{}">'
        "</div>",
        width,
        height,
        image.url,
        alt or "Превью изображения",
    )
