from django.conf import settings #todo fix MEDIA_URL usage
from django.db.models import Prefetch
import logging


logger = logging.getLogger("about")

def get_section_content(limit=1):
    from .models import AboutSection, AboutSectionFeatures, AboutSectionWidget
    content = (
        AboutSection.objects.prefetch_related(
            Prefetch(
                'features',
                queryset=AboutSectionFeatures.objects.filter(is_active=True),
            ),
            'images',
            Prefetch(
                'widget',
                queryset=AboutSectionWidget.objects.filter(is_active=True),
            ),
        )
        .filter(is_active=True)
        .first()
    )
    return {
        'content': content,
        'MEDIA_URL': settings.MEDIA_URL,
    }
