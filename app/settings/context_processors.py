import logging

from settings.models import SocialMedia

from .models import Landing

logger = logging.getLogger("settings")


def global_context(request):
    """
    Global context processor for Landing settings and navigation.

    Provides common data to all templates:
    - Landing settings (title, description, footer, avatar)
    - Anchors list
    - Social media links
    """
    logger.debug(f"Processing global context for path: {request.path}")

    # Получаем настройки блога
    try:
        settings = (
            Landing.objects.values(
                "title", "desc", "footer", "avatar"
            ).first()
            or {}
        )
        # anchors = BlockType.objects.all()
        # anchor_count = anchors.count()
        # logger.debug(f"Loaded {anchor_count} anchors")

        social_media = SocialMedia.objects.all()
        social_count = social_media.count()
        logger.debug(f"Loaded {social_count} social media links")

    except Exception as e:
        logger.error(f"Error loading context data: {e}", exc_info=True)
        #anchors = BlockType.objects.none()
        social_media = SocialMedia.objects.none()

    context = {
        #"anchors": anchors,
        "title": settings.get("title", ""),
        "about": settings.get("desc", ""),
        "footer": settings.get("footer", ""),
        "avatar": settings.get("avatar", ""),
        "social_media": social_media,
    }

    logger.debug("Global context processing completed")
    return context
