
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import order.models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CatalogFlower',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Название')),
                ('bouquet_composition', models.TextField(verbose_name='Состав букета')),
                ('description', models.TextField(verbose_name='Описание')),
                ('image', models.ImageField(upload_to='', verbose_name='Изображение')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Цена')),
            ],
            options={
                'verbose_name': 'букет',
                'verbose_name_plural': 'букеты',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Событие')),
            ],
            options={
                'verbose_name': 'категория',
                'verbose_name_plural': 'категории',
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=50, verbose_name='Имя')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True, verbose_name='Телефон')),

                ('email', models.EmailField(blank=True, max_length=50, verbose_name='Email')),
            ],
            options={
                'verbose_name': 'клиент',
                'verbose_name_plural': 'клиенты',
            },
        ),
        migrations.CreateModel(
            name='Florist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Имя')),
            ],
            options={
                'verbose_name': 'флорист',
                'verbose_name_plural': 'флористы',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_number', models.IntegerField(verbose_name='Номер карты')),
                ('cardholder', models.CharField(max_length=50, verbose_name='Имя владельца')),
                ('month', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(12), django.core.validators.MinValueValidator(1)], verbose_name='Месяц')),
                ('year', models.PositiveIntegerField(validators=[order.models.year_validator], verbose_name='Год')),
                ('cvc', models.CharField(max_length=3, validators=[django.core.validators.RegexValidator('^\\d{3}$', 'CVC должен состоять из 3 цифр.')], verbose_name='CVC')),
                ('email', models.EmailField(blank=True, max_length=50, verbose_name='Email')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField(max_length=100, verbose_name='Адрес')),
                ('delivery_time', models.CharField(choices=[('1', 'Как можно скорее'), ('2', 'с 10:00 до 12:00'), ('3', 'с 12:00 до 14:00'), ('4', 'с 14:00 до 16:00'), ('5', 'с 16:00 до 18:00'), ('6', 'c 18:00 до 20:00')], max_length=50, verbose_name='Время доставки')),

                ('status', models.CharField(choices=[('Новый', 'Новый'), ('Доставляется', 'Доставляется'), ('Доставлен', 'Доставлен')], db_index=True, default='Новый', max_length=50, verbose_name='Статус заказа')),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='order.client', verbose_name='Клиент')),
                ('florist', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='order.florist', verbose_name='Флорист')),
                ('flower', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='order.catalogflower', verbose_name='Букет')),
                ('payment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payments', to='order.payment', verbose_name='Оплата')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.CreateModel(
            name='Consultation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='дата консультации')),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='clients', to='order.client', verbose_name='Клиент')),
                ('florist', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='florists', to='order.florist', verbose_name='Флорист')),
            ],
            options={
                'verbose_name': 'консультация',
                'verbose_name_plural': 'консультации',
            },
        ),
        migrations.AddField(
            model_name='catalogflower',
            name='category',
            field=models.ManyToManyField(to='order.category', verbose_name='Категория'),
        ),
    ]
