from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from .models import Page

class PageView(DetailView):
    model = Page
    template_name = "page.html"
    context_object_name = "page"
    
    def get_queryset(self):
        return Page.objects.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blocks'] = self.object.blocks.filter(is_active=True).order_by('order')
        return context

def home(request):
    """Главная страница"""
    try:
        home_page = Page.objects.filter(is_active=True, slug='home').first()
        if home_page:
            return PageView.as_view()(request, slug='home')
    except:
        pass
    
    # Запасной вариант
    return render(request, 'home.html')