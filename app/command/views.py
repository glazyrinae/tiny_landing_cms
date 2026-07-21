from django.conf import settings #todo fix MEDIA_URL usage
from django.db.models import Prefetch
import logging


logger = logging.getLogger("command")

def get_section_content(limit=1):
    from .models import CommandSection, CommandSectionFeatures
    content = (
        CommandSection.objects.prefetch_related(
            Prefetch(
                'features',
                queryset=CommandSectionFeatures.objects.filter(is_active=True),
            )
        )
        .filter(is_active=True)
        .first()
    )
    return {
        'content': content,
        'MEDIA_URL': settings.MEDIA_URL,
    }
