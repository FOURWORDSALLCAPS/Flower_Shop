# Generated by Django 4.2.3 on 2023-08-24 14:14

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_remove_order_payment_alter_order_delivery_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catalogflower',
            name='price',
            field=models.DecimalField(db_index=True, decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Цена'),
        ),
    ]
