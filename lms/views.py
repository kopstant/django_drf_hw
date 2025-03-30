from rest_framework import viewsets, generics
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from lms.tasks import send_course_update_mail

from users.permissions import IsModeratorOrOwner, IsOwner
from .models import Lesson, Course
from users.models import SubscriptionForCourse
from .serializers import LessonSerializer, CourseSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """
    Управляет курсами.
    Модель CourseView.
    Контролирует доступ к курсам, разрешает модераторам просматривать и редактировать их, но не удалять и создавать.
    Is_moderator - кастомное разрешение.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_permissions(self):
        """
        Определяет права доступа применяются в зависимости от выполняемого действия.
        """
        if self.action in ['create', 'destroy']:
            permission_classes = [IsAuthenticated, IsOwner]  # Только владельцы могут создавать и удалять
        else:
            permission_classes = [IsAuthenticated, IsModeratorOrOwner]

        return [permission() for permission in permission_classes]

    def perform_update(self, serializer):
        """
        Обновление курса и отправка уведомления всем подписанным пользователям.
        """
        course = serializer.save()
        # Отправляем уведомление подписчикам (асинхронно)
        send_course_update_mail.delay(course.id)  # Вызываем задачу


class CourseSubscriptionViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')

        if not course_id:
            return Response({'error': 'Не указан id курса.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            return Response({'error': 'Course does not find.'}, status=status.HTTP_404_NOT_FOUND)

        subscription = SubscriptionForCourse.objects.filter(owner=user, course=course)

        if subscription.exists():
            subscription.delete()
            message = 'Подписка удалена'
        else:
            SubscriptionForCourse.objects.create(owner=user, course=course)
            message = 'Подписка добавлена'

        return Response({'message': message}, status=status.HTTP_200_OK)


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner]  # Только владельцы могут создавать

    def perform_create(self, serializer):
        course_id = self.request.data.get('course')
        try:
            course = Course.objects.get(pk=course_id)
            if course.owner != self.request.user:
                raise PermissionDenied("Вы не являетесь владельцем этого курса.")
        except Course.DoesNotExist:
            raise NotFound("Курс не найден.")
        serializer.save(owner=self.request.user, course=course)


class LessonListAPIView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]  # Авторизованные пользователи могут просматривать


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModeratorOrOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModeratorOrOwner]


class LessonDeleteAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]  # Только владельцы могут удалять
