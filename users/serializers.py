from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models import CustomUser, Payment

User = get_user_model()  # получает пользовательскую модель


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"

    def validate(self, data):
        """Проверяем, что указан либо курс, либо урок"""
        if not data.get("course") and not data.get("lesson"):
            raise serializers.ValidationError("Необходимо указать курс или урок")
        return data


class UserSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True, source="payment_set")

    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "phone", "city", "avatar", "payments"]


class RegisterSerializer(serializers.ModelSerializer):  # Сериализатор для создания новых пользователей.
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        """
        Cоздает пользователя, используя встроенный метод Django (который автоматически хеширует пароль).
        Возвращает созданного пользователя.
        """
        user = User.objects.create_user(
            username=validated_data["username"], email=validated_data["email"], password=validated_data["password"]
        )
        return user
