from django_filters.rest_framework import DjangoFilterBackend, filters
from rest_framework import viewsets
from users.models import CustomUser
from users.serializers import CustomUserSerializer, PaymentSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['course', 'lesson', 'payment_method']
    ordering_fields = ['date']
    ordering = ['-date']  # По умолчанию сортировка от новых к старым
