from django.conf import settings #todo fix MEDIA_URL usage
import logging


logger = logging.getLogger("price")

def get_section_content(limit=1):
    from .models import PriceSection
    content = PriceSection.objects.prefetch_related(
        'features'
    ).filter(is_active=True).first
    return {
        'content': content,
        'MEDIA_URL': settings.MEDIA_URL,
    }