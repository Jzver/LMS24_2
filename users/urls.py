from django.urls import path
from rest_framework.routers import DefaultRouter

from users.apps import UsersConfig
from users.views import UserViewSet, PaymentLiatAPIView

app_name = UsersConfig.name
router = DefaultRouter()
router.register(r"user", UserViewSet, basename="user")


urlpatterns = [
    path("payments/", PaymentLiatAPIView.as_view(), name="payments"),
] + router.urls