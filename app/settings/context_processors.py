import logging

from address.models import AddressSection
from settings.models import SocialMedia

from .models import Landing
from tiny_cms.seo import build_local_business_schema, get_landing_seo_context

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
    landing = (
        Landing.objects.values(
            "title", "desc", "footer", "avatar"
        ).first()
        or {}
    )
    seo_context = get_landing_seo_context(request, landing)
    structured_data = ""

    # Получаем настройки блога
    try:
        # anchors = BlockType.objects.all()
        # anchor_count = anchors.count()
        # logger.debug(f"Loaded {anchor_count} anchors")

        social_media = SocialMedia.objects.all()
        social_links = list(social_media.values_list("url_link", flat=True))
        address = AddressSection.objects.first()
        structured_data = build_local_business_schema(
            seo_context,
            address=address,
            social_links=social_links,
        )
        social_count = social_media.count()
        logger.debug(f"Loaded {social_count} social media links")

    except Exception as e:
        logger.error(f"Error loading context data: {e}", exc_info=True)
        #anchors = BlockType.objects.none()
        social_media = SocialMedia.objects.none()

    context = {
        #"anchors": anchors,
        "title": landing.get("title", ""),
        "about": landing.get("desc", ""),
        "footer": landing.get("footer", ""),
        "avatar": landing.get("avatar", ""),
        "social_media": social_media,
        "structured_data": structured_data,
        **seo_context,
    }

    logger.debug("Global context processing completed")
    return context
