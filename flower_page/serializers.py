from django.core.validators import RegexValidator
from rest_framework import serializers


class ClientSerializer(serializers.Serializer):
    firstname = serializers.CharField(max_length=100)
    phone = serializers.CharField(
        validators=[RegexValidator(
            regex=r'^\+?7?\d{10}$',
            message="Phone number must be entered in the format: '+799999999'. Up to 10 digits allowed."
        )]
    )


class OrderSerializer(serializers.Serializer):
    firstname = serializers.CharField(max_length=100)
    phone = serializers.CharField(
        validators=[RegexValidator(
            regex=r'^\+?7?\d{10}$',
            message="Phone number must be entered in the format: '+799999999'. Up to 10 digits allowed."
        )]
    )
    address = serializers.CharField(max_length=200)
    delivery_time = serializers.CharField()
    item_id = serializers.IntegerField()


class PaymnetSerializer(serializers.Serializer):
    card_number = serializers.CharField(
        validators=[RegexValidator(
            regex=r'^\d{16}$',
            message="Card number must be entered in the format: '1111222233334444'. Up to 16 digits allowed."
        )]
    )
    card_mm = serializers.CharField(
        validators=[RegexValidator(
            regex=r'^(0[1-9]|1[0-2])$',
            message="Month must be entered in the format: '01' to '12'."
        )]
    )
    card_gg = serializers.CharField(
        validators=[RegexValidator(
            regex=r'^(2[3-9]|[3-9][0-9])$',
            message="Year must be entered in the format: '2023' to '2099'."
        )]
    )
    card_firstname = serializers.CharField(
        validators=[RegexValidator(
            regex=r'^[A-Za-z]+ [A-Za-z]+$',
            message="Name must be entered in the format: 'Ivan Ivanov'."
        )]
    )
    card_cvc = serializers.CharField(
        validators=[RegexValidator(
            regex=r'^\d{3}$',
            message="CVC must be entered in the format: '123'. Up to 3 digits allowed."
        )]
    )
