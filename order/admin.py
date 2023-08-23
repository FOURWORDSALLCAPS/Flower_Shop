from django.contrib import admin
from django.utils.html import format_html

from .models import CatalogFlower, Client, Category, Florist, Consultation, Order, Payment


@admin.register(CatalogFlower)
class CatalogFlowerAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'bouquet_composition',
        'description',
        'display_categories',
        'price',
    ]

    readonly_fields = [
        'get_image_preview',
    ]

    def get_image_preview(self, obj):
        if not obj.image:
            return 'выберите картинку'
        return format_html('<img src="{url}" style="max-height: 200px;"/>', url=obj.image.url)

    get_image_preview.short_description = 'превью'

    def display_categories(self, obj):
        return ", ".join([category.title for category in obj.category.all()])

    display_categories.short_description = 'категория'


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = [
        'firstname',
        'phone',
        'email',
    ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'title',
    ]


@admin.register(Florist)
class FloristAdmin(admin.ModelAdmin):
    list_display = [
        'name',
    ]


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = [
        'client',
        'florist',
    ]


def get_flower_type(obj):
    if obj.catalog_flower:
        return "Букет из каталога"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'client',
        'flower',
        'address',
        'delivery_time',
        'status',
        'get_total_price'
    ]

    fields = [
        'client',
        'flower',
        'address',
        'delivery_time',
        'status',
        'get_total_price'
    ]

    readonly_fields = [
        'get_total_price',
    ]

    def has_change_permission(self, request, obj=None):
        if request.user.groups.filter(name='florists').exists():
            return True
        return False

    def get_total_price(self, obj):
        if obj.flower:
            return obj.flower.price

    get_total_price.short_description = 'Итоговая стоимость'


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    pass
