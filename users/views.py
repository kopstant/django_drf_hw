from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend, filters
from rest_framework import viewsets, generics, permissions

from lms.models import Lesson, Course
from lms.paginators import CustomPaginator
from lms.serializers import LessonSerializer
from users.models import CustomUser, Payment
from users.serializers import UserSerializer, PaymentSerializer, RegisterSerializer
from rest_framework.filters import OrderingFilter

User = get_user_model()  # получает пользовательскую модель


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