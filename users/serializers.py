from rest_framework import serializers
from users.models import Payment
from users.models import CustomUser


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class CustomUserSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True, source="payment_set")

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'phone', 'city', 'avatar', 'payments']
