from django.conf import settings #todo fix MEDIA_URL usage
import logging


logger = logging.getLogger("service")

def get_section_content(limit=1):
    from .models import ServiceSection
    content = ServiceSection.objects.prefetch_related('features').filter(is_active=True).first()
    return {
        'content': content,
        'MEDIA_URL': settings.MEDIA_URL,
    }