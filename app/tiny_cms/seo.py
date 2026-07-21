import json
import re
from urllib.parse import urljoin

from django.apps import apps
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Max
from django.utils.html import strip_tags


DEFAULT_SITE_URL = "https://fizruk-fitness.ru"
DEFAULT_SITE_NAME = "Физрук"
DEFAULT_SITE_TITLE = "Фитнес-клуб Физрук"
DEFAULT_SITE_DESCRIPTION = (
    "Фитнес-клуб Физрук: тренировки, персональные занятия, абонементы "
    "и консультации."
)
DEFAULT_LOGO_PATH = "/media/logo.jpg"
TRACKING_QUERY_PARAMS = (
    "utm_source",
    "utm_medium",
    "utm_campaign",
    "utm_content",
    "utm_term",
    "utm_referrer",
    "utm_media",
    "utm_group",
    "yclid",
    "ysclid",
    "gclid",
    "fbclid",
)


def clean_string(value):
    text = strip_tags(str(value or ""))
    return re.sub(r"\s+", " ", text).strip()


def normalize_meta_description(value, max_length=160):
    text = clean_string(value) or DEFAULT_SITE_DESCRIPTION
    if len(text) <= max_length:
        return text

    truncated = text[: max_length - 3].rsplit(" ", 1)[0].rstrip(".,;:- ")
    return f"{truncated or text[: max_length - 3]}..."


def get_site_url():
    site_url = (getattr(settings, "SITE_URL", "") or DEFAULT_SITE_URL).strip()
    if not site_url.startswith(("http://", "https://")):
        site_url = f"https://{site_url}"
    return site_url.rstrip("/")


def absolute_url(path="/"):
    path = str(path or "/")
    if path.startswith(("http://", "https://")):
        return path
    return urljoin(f"{get_site_url()}/", path.lstrip("/"))


def media_absolute_url(path):
    if not path:
        return absolute_url(DEFAULT_LOGO_PATH)

    media_url = getattr(settings, "MEDIA_URL", "/media/")
    return absolute_url(f"{media_url.rstrip('/')}/{str(path).lstrip('/')}")


def build_page_title(title):
    title = clean_string(title)
    if not title:
        return DEFAULT_SITE_TITLE
    if "фитнес" in title.lower():
        return title
    return f"Фитнес-клуб {title}"


def get_landing_seo_context(request=None, landing=None):
    landing = landing or {}
    site_name = clean_string(landing.get("title")) or DEFAULT_SITE_NAME
    description = normalize_meta_description(landing.get("desc"))
    canonical_path = getattr(request, "path", "/") or "/"
    logo = landing.get("avatar")

    return {
        "site_url": get_site_url(),
        "site_name": site_name,
        "seo_title": build_page_title(site_name),
        "seo_description": description,
        "canonical_url": absolute_url(canonical_path),
        "site_logo_url": media_absolute_url(logo),
    }


def build_local_business_schema(seo_context, address=None, social_links=None):
    schema = {
        "@context": "https://schema.org",
        "@type": "ExerciseGym",
        "@id": absolute_url("/#organization"),
        "name": seo_context["seo_title"],
        "url": absolute_url("/"),
        "description": seo_context["seo_description"],
        "logo": seo_context["site_logo_url"],
        "image": seo_context["site_logo_url"],
    }

    if address:
        phone = clean_string(getattr(address, "phone", ""))
        street_address = clean_string(getattr(address, "address", ""))
        if phone:
            schema["telephone"] = phone
        if street_address:
            schema["address"] = {
                "@type": "PostalAddress",
                "streetAddress": street_address,
                "addressCountry": "RU",
            }

    same_as = [
        url
        for url in (social_links or [])
        if str(url).startswith(("http://", "https://"))
    ]
    if same_as:
        schema["sameAs"] = same_as

    return json.dumps(
        schema,
        ensure_ascii=False,
        separators=(",", ":"),
        cls=DjangoJSONEncoder,
    ).replace("</", "<\\/")


def get_site_last_modified():
    latest = None
    model_names = (
        ("hero", "HeroSection"),
        ("hero", "HeroSectionMarkers"),
        ("about", "AboutSection"),
        ("about", "AboutSectionFeatures"),
        ("service", "ServiceSection"),
        ("service", "ServiceSectionFeatures"),
        ("command", "CommandSection"),
        ("command", "CommandSectionFeatures"),
        ("price", "PriceSection"),
        ("price", "PriceSectionFeatures"),
        ("address", "AddressSection"),
        ("address", "AddressSectionFeatures"),
    )

    for app_label, model_name in model_names:
        try:
            model = apps.get_model(app_label, model_name)
            value = model.objects.aggregate(updated=Max("updated_at"))["updated"]
        except Exception:
            continue
        if value and (latest is None or value > latest):
            latest = value

    return latest


def get_clean_param_value():
    return "&".join(TRACKING_QUERY_PARAMS)
