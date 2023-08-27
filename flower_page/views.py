import random
import stripe

from environs import Env
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.db import DatabaseError, OperationalError
from .serializers import OrderSerializer, PaymentSerializer, ClientSerializer
from django.db.models import F

from order.models import CatalogFlower, Order, Florist, Client, Consultation


def view_index(request) -> HttpResponse:
    recommendation_items = CatalogFlower.objects.filter().order_by('pk')[:3]

    return render(request, template_name='index.html', context={
        'recommendation_items': recommendation_items
    })


def view_catalog(request) -> HttpResponse:
    catalog_items = CatalogFlower.objects.all()
    if len(catalog_items) % 3 != 0:
        catalog_items = catalog_items[:9]
    return render(request, template_name='catalog.html', context={
        'catalog_items': catalog_items
    })


def view_consultation(request) -> HttpResponse:
    return render(request, template_name='consultation.html')


def view_order(request) -> HttpResponse:
    item_id = request.POST.get('item_id')
    if item_id:
        item = CatalogFlower.objects.filter(pk=item_id).first()
        return render(request, 'order.html', {'item': item})
    else:
        return redirect('/catalog')


def view_order_step(request) -> HttpResponse:
    if request.method == "POST":
        serializer_order = OrderSerializer(data=request.POST)
        if not serializer_order.is_valid():
            messages.error(request, 'Проверьте корректность вводимых данных')
        else:
            validated_data = serializer_order.validated_data
            firstname = validated_data['firstname']
            item = CatalogFlower.objects.filter(pk=validated_data['item_id']).first()
            try:
                client, client_created = Client.objects.get_or_create(
                    phone=validated_data['phone'], defaults={'firstname': firstname}
                )

                if not client_created and client.firstname != firstname:
                    client.update(firstname=F(firstname))

                order, created = Order.objects.get_or_create(
                    client=client,
                    flower=item,
                    florist_id=random.choice(Florist.objects.values_list('id', flat=True)),
                    address=validated_data['address'],
                    delivery_time=validated_data['delivery_time'],
                )
                if created:
                    pass  # TODO Заглушка для вывода окна об успешном создании заказа!
            except (DatabaseError, OperationalError) as e:
                return JsonResponse({'error': str(e)}, status=500)

            return render(request, 'order-step.html', {'order_id': order.id})

    return render(request, 'order.html')


def view_quiz(request) -> HttpResponse:
    return render(request, template_name='quiz.html')


def view_quiz_step(request) -> HttpResponse:
    if request.method == "POST":
        quiz_category = request.POST.get("button_quiz")
        if quiz_category is not None:
            request.session['quiz_category'] = quiz_category
    return render(request, template_name='quiz-step.html')


def view_result(request) -> HttpResponse:
    if request.method == "POST":
        quiz_price_range = request.POST.get("button_quiz_step")
        quiz_category = request.session.get('quiz_category')
        price_ranges = {
            '1000': {'price__lt': '1000'},
            '1001': {'price__gt': '1000', 'price__lt': '5000'},
            '5000': {'price__gt': '5000'},
        }
        if quiz_price_range in price_ranges:
            filters = price_ranges[quiz_price_range]
            filters['category__title'] = quiz_category
            card_item = CatalogFlower.objects.filter(**filters)[:3]
        else:
            card_item = CatalogFlower.objects.all()[:3]
        return render(request, template_name='result.html', context={'card_item': card_item})


def view_card(request, card_id) -> HttpResponse:
    card_item = CatalogFlower.objects.filter(id=card_id)
    return render(request, template_name='card.html', context={
        'card_item': card_item
    })


def make_payment(card_number, exp_month, exp_year, cvc):
    env = Env()
    env.read_env()
    stripe.api_key = env('STRIPE_API_KEY')
    try:
        token = stripe.Token.create(
            card={
                'number': card_number,
                'exp_month': exp_month,
                'exp_year': exp_year,
                'cvc': cvc
            }
        )
        charge = stripe.Charge.create(
            amount=1000,
            currency='usd',
            source=token.id
        )
        if charge.paid:
            return True
    except stripe.error.CardError as e:
        return False
    except stripe.error.StripeError as e:
        return False


def process_payment(request) -> HttpResponse:
    if request.method == "POST":
        order_id = request.POST.get('order_id')
        serializer_payment = PaymentSerializer(data=request.POST)
        if not serializer_payment.is_valid():
            messages.error(request, 'Проверьте корректность вводимых данных')
            return render(request, 'order-step.html', {'order_id': order_id})
        else:
            card_number = request.POST.get('card_number')
            exp_month = request.POST.get('card_mm')
            exp_year = request.POST.get('card_gg')
            cvc = request.POST.get('card_cvc')
            if make_payment(card_number, exp_month, exp_year, cvc):
                order = get_object_or_404(Order, id=order_id)
                order.status = "Оплачено"
                order.save()
                # TODO Заглушка для вывода окна об успешной оплате заказа!
                return redirect('/')


def consultation_post(request) -> HttpResponse:
    if request.method == "POST":
        serializer_client = ClientSerializer(data=request.POST)
        if not serializer_client.is_valid():
            messages.error(request, 'Проверьте корректность вводимых данных')
        else:
            validated_data = serializer_client.validated_data
            firstname = validated_data['firstname']
            try:
                client, created = Client.objects.get_or_create(
                    phone=validated_data['phone'],
                    defaults={'firstname': firstname}
                )
                if not created and client.firstname != firstname:
                    client.update(firstname=F(firstname))
                consultation, client_created = Consultation.objects.get_or_create(
                    client=client,
                    florist_id=random.choice(Florist.objects.values_list('id', flat=True)),
                )
                if client_created:
                    pass  # TODO Заглушка для вывода окна об успешном создании консультации!
            except (DatabaseError, OperationalError) as e:
                return JsonResponse({'error': str(e)}, status=500)
    return redirect('/#consultation')
