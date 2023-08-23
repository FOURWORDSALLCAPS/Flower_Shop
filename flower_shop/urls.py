from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from flower_page.views import view_index

from . import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', view_index),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
