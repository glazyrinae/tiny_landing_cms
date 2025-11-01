# project_name/views.py (в корне проекта)
from django.shortcuts import render

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