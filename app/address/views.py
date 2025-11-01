from django.conf import settings #todo fix MEDIA_URL usage
import logging


logger = logging.getLogger("address")

def get_section_content(limit=1):
    from .models import AddressSection
    content = AddressSection.objects.prefetch_related('features').first()
    return {
        'content': content,
        'MEDIA_URL': settings.MEDIA_URL,
    }