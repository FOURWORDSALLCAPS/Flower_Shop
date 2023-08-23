from datetime import datetime
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.utils import timezone
from django.db import models


def year_validator():
    current_year = datetime.now().year
    return MinValueValidator(current_year)


class Client(models.Model):
    firstname = models.CharField('Имя', max_length=50)
    phone = PhoneNumberField('Телефон')
    email = models.EmailField('Email', max_length=50, blank=True)

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'

    def __str__(self):
        return self.firstname


class CatalogFlower(models.Model):
    title = models.CharField('Название', max_length=50)
    bouquet_composition = models.TextField('Состав букета')
    description = models.TextField('Описание')
    image = models.ImageField('Изображение')
    category = models.ManyToManyField('Category', verbose_name='Категория')
    price = models.DecimalField('Цена', max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])

    class Meta:
        verbose_name = 'букет'
        verbose_name_plural = 'букеты'

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField('Событие', max_length=50)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.title


class Florist(models.Model):
    name = models.CharField('Имя', max_length=50)

    class Meta:
        verbose_name = 'флорист'
        verbose_name_plural = 'флористы'

    def __str__(self):
        return self.name


class Consultation(models.Model):
    client = models.ForeignKey(
        Client,
        verbose_name='Клиент',
        related_name='clients',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    florist = models.ForeignKey(
        Florist,
        verbose_name='Флорист',
        related_name='florists',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    create_at = models.DateTimeField(
        'дата оформления заказа',
        default=timezone.now,
        blank=True
    )

    class Meta:
        verbose_name = 'консультация'
        verbose_name_plural = 'консультации'


class Payment(models.Model):
    cvc_validator = RegexValidator(r'^\d{3}$', "CVC должен состоять из 3 цифр.")
    card_number = models.IntegerField('Номер карты')
    cardholder = models.CharField('Имя владельца', max_length=50)
    month = models.PositiveSmallIntegerField(
        'Месяц',
        validators=[
            MaxValueValidator(12),
            MinValueValidator(1)
        ])
    year = models.PositiveIntegerField('Год', validators=[year_validator])
    cvc = models.CharField('CVC', max_length=3, validators=[cvc_validator])
    email = models.EmailField('Email', max_length=50, blank=True)


class Order(models.Model):
    TIME_CHOICES = (
        ('1', 'Как можно скорее'),
        ('2', 'с 10.00 до 12:00'),
        ('3', 'с 12:00 до 14:00'),
        ('4', 'с 14:00 до 16:00'),
        ('5', 'с 16:00 до 18:00'),
        ('6', 'c 18:00 до 20:00'),
    )

    class ChoicesStatus(models.TextChoices):
        NEW = 'Новый', 'Новый'
        DELIVERED = 'Доставляется', 'Доставляется'
        ACCEPT = 'Доставлен', 'Доставлен'

    client = models.ForeignKey(Client, verbose_name='Клиент', on_delete=models.SET_NULL, null=True)
    flower = models.ForeignKey(CatalogFlower, verbose_name='Букет', on_delete=models.SET_NULL, null=True)
    florist = models.ForeignKey(Florist, verbose_name='Флорист', on_delete=models.SET_NULL, null=True)
    address = models.TextField('Адрес', max_length=100)
    delivery_time = models.CharField('Время доставки', max_length=50, choices=TIME_CHOICES)
    status = models.CharField('Статус заказа', max_length=50, choices=ChoicesStatus.choices, default=ChoicesStatus.NEW, db_index=True)
    payment = models.ForeignKey(Payment, verbose_name='Оплата', related_name='payments', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
