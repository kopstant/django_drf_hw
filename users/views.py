import stripe
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, permissions, status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from lms.models import Lesson, Course
from lms.paginators import CustomPaginator
from lms.serializers import LessonSerializer
from users.models import CustomUser, Payment
from users.serializers import UserSerializer, PaymentSerializer, RegisterSerializer
from rest_framework.filters import OrderingFilter

User = get_user_model()  # получает пользовательскую модель
stripe.api_key = settings.STRIPE_API_KEY


class CustomUserViewSet(viewsets.ModelViewSet):
    """
    Управляет пользователями.
    Модель CustomUser.
    Позволяет создавать, изменять, удалять и просматривать пользователей.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]  # Настройка прав доступа. Доступ только для аутентифицированных пользователей.


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['payment_method']
    ordering_fields = ['date']
    ordering = ['-date']  # По умолчанию сортировка от новых к старым


class UserListCreateView(generics.ListCreateAPIView):  # Позволяет просматривать список пользователей и создавать нового
    queryset = User.objects.all()  # выбрать всех пользователей из БД.
    serializer_class = UserSerializer  # преобразует данные при помощи UserSerializer
    permission_classes = [
        permissions.IsAuthenticated]  # Настройка прав доступа. Доступ только для аутентифицированных пользователей.


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):  # GET, PUT/PATCH, DELETE
    queryset = User.objects.all()  # выбрать всех пользователей из БД.
    serializer_class = UserSerializer  # преобразует данные при помощи UserSerializer
    permission_classes = [
        permissions.IsAuthenticated]  # Настройка прав доступа. Доступ только для аутентифицированных пользователей.


class RegisterView(generics.CreateAPIView):  # Позволяет создавать нового пользователя (зарегистрировать) POST
    queryset = User.objects.all()
    serializer_class = RegisterSerializer  # хэширование пароля при помощи RegisterSerializer
    permission_classes = [permissions.AllowAny]  # Доступ без авторизации. Для регистрации.


class LessonListAPIView(generics.ListAPIView):  # Пагинация для уроков
    queryset = Lesson.objects.all()  # Выбрать все уроки из БД.
    serializer_class = LessonSerializer  # Преобразует данные при помощи LessonSerializer
    pagination_class = CustomPaginator  # Пагинация


class CourseListAPIView(generics.ListAPIView):  # Пагинация для курсов
    queryset = Course.objects.all()  # Выбрать все курсы из БД.
    serializer_class = LessonSerializer  # Преобразует данные при помощи LessonSerializer
    pagination_class = CustomPaginator  # Пагинация


class PaymentCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            payment = serializer.save(user=request.user)

            try:
                payment_link, payment_id = payment.create_stripe_payment(request)
                payment.session_id = payment_id
                payment.link = payment_link
                payment.save()
                return Response({
                    'payment_id': payment_id,
                    'payment_link': payment_link,
                    'status': 'created'
                }, status=status.HTTP_201_CREATED)
            except ValueError as e:
                payment.delete()
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentSuccessView(APIView):
    """View для обработки успешной оплаты"""

    def get(self, request, pk, *args, **kwargs):
        payment = get_object_or_404(Payment, pk=pk)

        # Проверяем статус платежа в Stripe
        try:
            session = stripe.checkout.Session.retrieve(payment.session_id)

            if session.payment_status == 'paid':
                payment.is_paid = True
                payment.save()
                return Response({'status': 'success', 'message': 'Платеж успешно завершен'})
            else:
                return Response({'status': 'pending', 'message': 'Ожидается оплата'})

        except stripe.error.StripeError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PaymentCancelView(APIView):
    """View для обработки отмены оплаты"""

    def get(self, request, pk, *args, **kwargs):
        return Response({'status': 'canceled', 'message': 'Оплата отменена'})
