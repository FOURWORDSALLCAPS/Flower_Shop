# Generated by Django 4.2.3 on 2023-08-25 13:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_alter_catalogflower_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consultation',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='clients', to='order.client', verbose_name='Клиент'),
        ),
        migrations.AlterField(
            model_name='order',
            name='client',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='order.client', verbose_name='Клиент'),
        ),
    ]