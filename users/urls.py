from django.urls import path, include
from rest_framework.routers import DefaultRouter
from lms.apps import LmsConfig
from lms.views import CourseViewSet
from .views import PaymentViewSet

app_name = LmsConfig.name
router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
                  path('', include(router.urls)),
              ] + router.urls
