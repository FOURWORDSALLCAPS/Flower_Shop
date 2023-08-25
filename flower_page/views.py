import random

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .serializers import OrderSerializer, PaymnetSerializer, ClientSerializer

from order.models import CatalogFlower, Order, Florist, Client, Consultation


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
    item_id = request.POST.get('item_id')
    if item_id:
        item = CatalogFlower.objects.get(pk=item_id)
        return render(request, 'order.html', {'item': item})
    else:
        return redirect('/catalog')


def view_order_step(request):
    if request.method == "POST":
        serializer_order = OrderSerializer(data=request.POST)
        if not serializer_order.is_valid():
            return JsonResponse(serializer_order.errors, status=400)
        validated_data = serializer_order.validated_data
        firstname = validated_data['firstname']
        item = CatalogFlower.objects.filter(pk=validated_data['item_id']).first()
        client, client_created = Client.objects.get_or_create(
            phone=validated_data['phone'], defaults={'firstname': firstname}
        )
        if not client_created and client.firstname != firstname:
            client.firstname = firstname
            client.save()
        order, created = Order.objects.get_or_create(
            client=client,
            flower=item,
            florist_id=random.choice(Florist.objects.values_list('id', flat=True)),
            address=validated_data['address'],
            delivery_time=validated_data['delivery_time'],
        )
        return render(request, 'order-step.html', {'order': order})

    return render(request, 'order.html')


def view_quiz(request):
    return render(request, template_name='quiz.html')


def view_quiz_step(request):
    if request.method == "POST":
        quiz_category = request.POST.get("button_quiz")
        request.session['quiz_category'] = quiz_category
    return render(request, template_name='quiz-step.html')


def view_result(request):
    if request.method == "POST":
        quiz_price_range = request.POST.get("button_quiz_step")
        quiz_category = request.session.get('quiz_category')
        if quiz_price_range == '1000':
            card_item = CatalogFlower.objects.filter(category__title=quiz_category, price__lt=quiz_price_range)[:3]
        elif quiz_price_range == '1001':
            card_item = CatalogFlower.objects.filter(category__title=quiz_category, price__gt=quiz_price_range, price__lt='5000')[:3]
        elif quiz_price_range == '5000':
            card_item = CatalogFlower.objects.filter(category__title=quiz_category, price__gt=quiz_price_range)[:3]
        else:
            card_item = CatalogFlower.objects.filter().order_by()[:3]
        return render(request, template_name='result.html', context={
            'card_item': card_item
        })
    return redirect('/')


def view_card(request, card_id):
    card_item = CatalogFlower.objects.filter(id=card_id)
    return render(request, template_name='card.html', context={
        'card_item': card_item
    })


def process_payment(request):
    if request.method == "POST":
        serializer_payment = PaymnetSerializer(data=request.POST)
        if not serializer_payment.is_valid():
            return JsonResponse(serializer_payment.errors, status=400)
        order_id = request.POST.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        order.status = "Оплачено"
        order.save()
        return redirect('/')

    return redirect('/order_step/')


def consultation_post(request):
    if request.method == "POST":
        serializer_client = ClientSerializer(data=request.POST)
        if not serializer_client.is_valid():
            return JsonResponse(serializer_client.errors, status=400)
        validated_data = serializer_client.validated_data
        client, client_created = Client.objects.get_or_create(
            phone=validated_data['phone'],
            defaults={'firstname': validated_data['firstname']}
        )
        if not client_created and client.firstname != validated_data['firstname']:
            client.firstname = validated_data['firstname']
            client.save()
        Consultation.objects.get_or_create(
            client=client,
            florist_id=random.choice(Florist.objects.values_list('id', flat=True)),
        )
        return redirect('/')
