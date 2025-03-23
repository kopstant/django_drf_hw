from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from lms.apps import LmsConfig
from .views import PaymentViewSet, RegisterView, CustomUserViewSet

app_name = LmsConfig.name
router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'users', CustomUserViewSet, basename='user')

urlpatterns = [
                  path('register/', RegisterView.as_view(), name='register'),
                  path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh')] + router.urls
