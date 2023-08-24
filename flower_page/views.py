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


def view_quiz(request):
    return render(request, template_name='quiz.html')


def view_quiz_step(request):
    return render(request, template_name='quiz-step.html')


def view_result(request):
    return render(request, template_name='result.html')


def view_card(request, card_id):
    card_item = CatalogFlower.objects.filter(id=card_id)
    return render(request, template_name='card.html', context={
        'card_item': card_item
    })
