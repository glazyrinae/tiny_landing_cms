from django.conf import settings #todo fix MEDIA_URL usage
import logging


logger = logging.getLogger("about")

def get_section_content(limit=1):
    from .models import AboutSection
    content = AboutSection.objects.prefetch_related('features', 'images', 'widget').filter(is_active=True).first()
    return {
        'content': content,
        'MEDIA_URL': settings.MEDIA_URL,
    }