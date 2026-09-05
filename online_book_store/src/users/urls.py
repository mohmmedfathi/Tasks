from django.urls import path

from .api import RegisterView

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
]
