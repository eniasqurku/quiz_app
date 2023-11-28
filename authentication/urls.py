from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from authentication.views import ChangePasswordView, Register

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    path(
        "creator/register/",
        Register.as_view(),
        name="register-creator",
        kwargs={"creator": True},
    ),
    path(
        "participant/register/",
        Register.as_view(),
        name="register-participant",
        kwargs={"creator": False},
    ),
]
