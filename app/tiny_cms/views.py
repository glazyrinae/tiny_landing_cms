from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.decorators.http import require_GET, require_http_methods

from settings.models import CallbackRequest
from .seo import absolute_url, get_clean_param_value, get_site_last_modified


@require_http_methods(["POST"])
def send_feedback(request):
    name = request.POST.get('name', '').strip()
    phone = request.POST.get('phone', '').strip()
    message = request.POST.get('message', '').strip()

    if not name or not phone:
        return JsonResponse({'error': 'Имя и телефон обязательны'}, status=400)

    CallbackRequest.objects.create(name=name, phone=phone, message=message)
    return JsonResponse({'status': 'ok'})


def main(request):
    """
    Главная страница проекта
    """
    blocks_config = [
        {'type': 'hero', 'params': {'limit': 1}},
        {'type': 'about', 'params': {'limit': 1}},
        {'type': 'service', 'params': {'limit': 3}},
        {'type': 'command', 'params': {'limit': 4}},
        {'type': 'price', 'params': {'limit': 5}},
        {'type': 'address', 'params': {'limit': 1}},
        # {'type': 'news', 'params': {'count': 3}},
    ]
    
    return render(request, 'base/_main.html', {
        'blocks': blocks_config
    })


@require_GET
def robots_txt(request):
    content = render_to_string(
        "seo/robots.txt",
        {
            "clean_param": get_clean_param_value(),
            "sitemap_url": absolute_url("/sitemap.xml"),
        },
    )
    return HttpResponse(content, content_type="text/plain; charset=utf-8")


@require_GET
def sitemap_xml(request):
    last_modified = get_site_last_modified()
    content = render_to_string(
        "seo/sitemap.xml",
        {
            "home_url": absolute_url("/"),
            "lastmod": last_modified.date().isoformat() if last_modified else "",
        },
    )
    return HttpResponse(content, content_type="application/xml; charset=utf-8")
