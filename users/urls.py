from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from lms.apps import LmsConfig
from .views import PaymentViewSet, RegisterView, CustomUserViewSet, PaymentCreateAPIView, PaymentSuccessView, PaymentCancelView

app_name = LmsConfig.name
router = DefaultRouter()
router.register(r"payments", PaymentViewSet, basename="payment")
router.register(r"users", CustomUserViewSet, basename="user")

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("payments/create/", PaymentCreateAPIView.as_view(), name="create_payment"),
    path("payments/success/<int:pk>/", PaymentSuccessView.as_view(), name="payment_success"),
    path("payments/cancel/<int:pk>/", PaymentCancelView.as_view(), name="payment_cancel"),
] + router.urls
