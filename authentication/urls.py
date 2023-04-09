from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from authentication.views import MyTokenObtainPairView, ChangePasswordView, Register

urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),

    path('creator/register/', Register.as_view(), name='creator', kwargs={'creator': True}),
    path('participant/register/', Register.as_view(), name='participant', kwargs={'creator': False}),
]
