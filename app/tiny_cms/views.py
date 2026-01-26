import os
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
import requests
import logging

# Путь к файлу с подписчиками
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SUBSCRIBERS_FILE =  "/app/shared/subscribers.json" #os.path.join(BASE_DIR, 'subscribers.json')

BOT_TOKEN = '8401349380:AAH09bxeMtEYHcDCLOw0Ge6USpeLqY2Aj8E'
# CHAT_ID тебе больше не нужен — рассылаем всем из файла


logger = logging.getLogger("tiny_cms")

def load_subscribers():
    if os.path.exists(SUBSCRIBERS_FILE):
        with open(SUBSCRIBERS_FILE) as f:
            return json.load(f)
    return []

@csrf_exempt
@require_http_methods(["POST"])
def send_feedback(request):
    name = request.POST.get('name', '').strip()
    phone = request.POST.get('phone', '').strip()
    message = request.POST.get('message', '').strip()

    if not name or not phone:
        return JsonResponse({'error': 'Имя и телефон обязательны'}, status=400)

    # Формируем текст
    text = f"📞 Новая заявка на звонок:\n\nИмя: {name}\nТелефон: {phone}\nСообщение: {message or '—'}"

    # Загружаем всех подписчиков
    subscribers = load_subscribers()
    if not subscribers:
        return JsonResponse({'error': 'Нет подписчиков для рассылки'}, status=500)

    # Рассылаем каждому
    failed = 0
    for user_id in subscribers:
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            resp = requests.post(url, json={"chat_id": user_id, "text": text}, timeout=10)
            logger.info(f"Response - {resp}")
            if resp.status_code != 200:
                failed += 1
        except Exception:
            failed += 1

    return JsonResponse({
        'status': 'ok',
        'sent_to': len(subscribers),
        'failed': failed
    })


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