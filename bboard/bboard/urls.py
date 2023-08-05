from django.contrib import admin
from django.conf import settings
from django.contrib.staticfiles.views import serve
from django.urls import path, include
from django.views.decorators.cache import never_cache
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'favicon.ico/',
        RedirectView.as_view(url='/static/icons/favicon.png', permanent=True)
    ),
    path('', include('main.urls')),
]

if settings.DEBUG:
    urlpatterns += [path('static/<path:path>', never_cache(serve))]
