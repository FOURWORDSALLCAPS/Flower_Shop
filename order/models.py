from datetime import datetime
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.db import models


def year_validator():
    current_year = datetime.now().year
    return MinValueValidator(current_year)


class Client(models.Model):
    firstname = models.CharField('Имя', max_length=50)
    phone = PhoneNumberField('Телефон', unique=True)
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
    price = models.DecimalField('Цена', max_digits=8, decimal_places=2, db_index=True, validators=[MinValueValidator(0)])

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
        'дата консультации',
        default=timezone.now,
        blank=True
    )

    class Meta:
        verbose_name = 'консультация'
        verbose_name_plural = 'консультации'


class Order(models.Model):
    TIME_CHOICES = (
        ('Как можно скорее', 'Как можно скорее'),
        ('с 10:00 до 12:00', 'с 10:00 до 12:00'),
        ('с 12:00 до 14:00', 'с 12:00 до 14:00'),
        ('с 14:00 до 16:00', 'с 14:00 до 16:00'),
        ('с 16:00 до 18:00', 'с 16:00 до 18:00'),
        ('с 18:00 до 20:00', 'с 18:00 до 20:00'),
    )

    class ChoicesStatus(models.TextChoices):
        NEW = 'Новый', 'Новый'
        Paid = 'Оплачено', 'Оплачено'
        DELIVERED = 'Доставляется', 'Доставляется'
        ACCEPT = 'Доставлен', 'Доставлен'

    client = models.ForeignKey(Client, verbose_name='Клиент', on_delete=models.SET_NULL, null=True)
    flower = models.ForeignKey(CatalogFlower, verbose_name='Букет', on_delete=models.SET_NULL, null=True)
    florist = models.ForeignKey(Florist, verbose_name='Флорист', on_delete=models.SET_NULL, null=True)
    address = models.TextField('Адрес', max_length=100)
    delivery_time = models.CharField('Время доставки', max_length=50, choices=TIME_CHOICES)
    status = models.CharField('Статус заказа', max_length=50, choices=ChoicesStatus.choices, default=ChoicesStatus.NEW, db_index=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
