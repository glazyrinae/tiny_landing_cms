from django.conf import settings #todo fix MEDIA_URL usage
from django.db.models import Prefetch
import logging


logger = logging.getLogger("hero")

def get_section_content(limit=1):
    from .models import HeroSection, HeroSectionMarkers
    content = (
        HeroSection.objects.prefetch_related(
            Prefetch(
                'markers',
                queryset=HeroSectionMarkers.objects.filter(is_active=True),
            )
        )
        .filter(is_active=True)
        .first()
    )
    return {
        'content': content,
        'MEDIA_URL': settings.MEDIA_URL,
    }
