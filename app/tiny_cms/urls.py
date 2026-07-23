"""
URL configuration for tiny_cms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import RedirectView
from .views import main, robots_txt, send_feedback, sitemap_xml  # из приложения core

admin.site.site_header = 'Админка физрук'
admin.site.site_title = 'Админка физрук'
admin.site.index_title = 'Админка физрук'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('robots.txt', robots_txt, name='robots_txt'),
    path('sitemap.xml', sitemap_xml, name='sitemap_xml'),
    path(
        'favicon.ico',
        RedirectView.as_view(url='/media/logo.jpg', permanent=True),
        name='favicon',
    ),
    path('send-feedback/', send_feedback, name='send_feedback'),
    path('', main, name='main'),  # главная страница
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
