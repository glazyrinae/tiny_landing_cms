from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import render

from settings.models import CallbackRequest


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
