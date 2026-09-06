from django.urls import path
from rest_framework_simplejwt.views import TokenBlacklistView

from .api import LoginView, RefreshView, RegisterView

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/refresh/", RefreshView.as_view(), name="refresh"),
    path("auth/logout/", TokenBlacklistView.as_view(), name="logout"),
]
