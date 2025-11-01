from django.conf import settings #todo fix MEDIA_URL usage
import logging


logger = logging.getLogger("hero")

def get_section_content(limit=1):
    from .models import HeroSection
    content = HeroSection.objects.prefetch_related('markers').filter(is_active=True).first()
    return {
        'content': content,
        'MEDIA_URL': settings.MEDIA_URL,
    }