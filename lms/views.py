from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from users.permissions import IsModeratorOrOwner
from .models import Lesson, Course
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
    permission_classes = [IsAuthenticated, IsModeratorOrOwner]  # Проверяет принадлежит ли пользователь к группе модераторов

    def get_permissions(self):
        """
        Определяет права доступа применяются в зависимости от выполняемого действия.
        """
        if self.action in ['list', 'retrieve', 'update', 'partial_update']:
            return [IsAuthenticated(), IsModeratorOrOwner()]
        return [IsAuthenticated()]


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModeratorOrOwner]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]


class LessonUpdateAPIView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModeratorOrOwner]


class LessonDeleteAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModeratorOrOwner]


class LessonViewSet(viewsets.ModelViewSet):
    """
    Управляет уроками.
    Модель LessonView.

    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModeratorOrOwner]

    def get_permissions(self):
        """
        Определяет права доступа применяются в зависимости от выполняемого действия.
        """
        if self.action in ['list', 'retrieve', 'update', 'partial_update']:
            return [IsAuthenticated(), IsModeratorOrOwner()]
        return [IsAuthenticated()]


