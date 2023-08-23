from django.shortcuts import render

from order.models import CatalogFlower


def view_index(request):
    recommendation_items = CatalogFlower.objects.filter().order_by('pk')[:3]

    return render(request, template_name='index.html', context={
        'recommendation_items': recommendation_items
    })


def view_catalog(request):
    catalog_items = CatalogFlower.objects.all()

    return render(request, template_name='catalog.html', context={
        'catalog_items': catalog_items
    })


def view_consultation(request):
    return render(request, template_name='consultation.html')


def view_order(request):
    return render(request, template_name='order.html')


def view_order_step(request):
    return render(request, template_name='order-step.html')