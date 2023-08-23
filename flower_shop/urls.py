from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from flower_page.views import view_index, view_catalog, view_consultation, view_order, view_order_step

from . import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', view_index),
    path('catalog/', view_catalog),
    path('consultation/', view_consultation),
    path('order/', view_order),
    path('order_step/', view_order_step),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
