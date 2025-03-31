from django.urls import path
from rest_framework.routers import DefaultRouter

from lms.apps import LmsConfig

from .views import (
    CourseSubscriptionViewSet,
    CourseViewSet,
    LessonCreateAPIView,
    LessonDeleteAPIView,
    LessonListAPIView,
    LessonRetrieveAPIView,
    LessonUpdateAPIView,
)

app_name = LmsConfig.name
router = DefaultRouter()
router.register(r"courses", CourseViewSet, basename="courses")

urlpatterns = [
    path("lessons/", LessonListAPIView.as_view(), name="lesson-list"),
    path("lessons/create/", LessonCreateAPIView.as_view(), name="lesson-create"),
    path("lessons/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson-get"),
    path("lessons/<int:pk>/update/", LessonUpdateAPIView.as_view(), name="lesson-update"),
    path("lessons/<int:pk>/delete/", LessonDeleteAPIView.as_view(), name="lesson-delete"),
    path("subscriptions/", CourseSubscriptionViewSet.as_view(), name="subscriptions"),
] + router.urls
