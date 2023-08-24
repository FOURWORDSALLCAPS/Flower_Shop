# Generated by Django 4.2.3 on 2023-08-24 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_time',
            field=models.CharField(choices=[('Как можно скорее', 'Как можно скорее'), ('с 10:00 до 12:00', 'с 10:00 до 12:00'), ('с 12:00 до 14:00', 'с 12:00 до 14:00'), ('с 14:00 до 16:00', 'с 14:00 до 16:00'), ('с 16:00 до 18:00', 'с 16:00 до 18:00'), ('с 18:00 до 20:00', 'с 18:00 до 20:00')], max_length=50, verbose_name='Время доставки'),
        ),
    ]
