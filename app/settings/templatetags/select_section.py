from django import template
from django.apps import apps
import importlib

register = template.Library()

@register.simple_tag()
def select_section(block_type, limit):
    """
    Динамически выбирает блок по типу
    """
    block_registry = {
        'hero': {
            'app': 'hero',
            'view': 'get_section_content',
            'template': 'hero/content.html'
        },
        'about': {
            'app': 'about',
            'view': 'get_section_content',
            'template': 'about/content.html'
        },
        'service': {
            'app': 'service',
            'view': 'get_section_content',
            'template': 'service/content.html'
        },
        'command': {
            'app': 'command', 
            'view': 'get_section_content',
            'template': 'command/content.html'
        },
        'price': {
            'app': 'price', 
            'view': 'get_section_content',
            'template': 'price/content.html'
        },
        'address': {
            'app': 'address', 
            'view': 'get_section_content',
            'template': 'address/content.html'
        },
    }
    
    if block_type not in block_registry:
        return f"<!-- Unknown block type: {block_type} -->"
    
    config = block_registry[block_type]
    
    try:
        # Импортируем функцию из приложения
        view_module = importlib.import_module(f"{config['app']}.views")
        view_func = getattr(view_module, config['view'])
        
        # Получаем контекст
        block_context = view_func(limit)
        
        # Рендерим шаблон
        return template.loader.render_to_string(
            config['template'],
            context={**block_context}
        )
    except Exception as e:
        return f"<!-- Error in {block_type}: {e} -->"