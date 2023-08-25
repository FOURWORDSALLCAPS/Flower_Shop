from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from flower_page.views import view_index, view_catalog, view_consultation, \
    view_order, view_order_step, view_quiz, view_quiz_step, view_result, view_card, process_payment

from . import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', view_index),
    path('catalog/', view_catalog),
    path('consultation/', view_consultation),
    path('order/', view_order),
    path('order_step/', view_order_step),
    path('quiz/', view_quiz),
    path('quiz_step/', view_quiz_step),
    path('result/', view_result),
    path('card/<int:card_id>', view_card),
    path('process_payment/', process_payment, name='process_payment'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
