from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from web import settings

urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    path('', include('main.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
