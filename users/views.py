from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend, filters
from rest_framework import viewsets, generics, permissions
from rest_framework.permissions import IsAuthenticated

from lms.models import Course, Lesson
from lms.serializers import CourseSerializer, LessonSerializer
from users.models import CustomUser
from users.permissions import IsModerator
from users.serializers import UserSerializer, PaymentSerializer, RegisterSerializer

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
        permissions.IsAuthenticated]  # Настройка прав доступа. Доступ только для аутентифицированных пользователей.


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['course', 'lesson', 'payment_method']
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
