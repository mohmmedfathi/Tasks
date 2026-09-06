import pytest
from django.urls import reverse
from rest_framework import status

from tests.constants import (
    USER_EMAIL_1,
    USER_PASSWORD_1,
    USER_USERNAME_1,
    USER_USERNAME_2,
)
from users.models import User


@pytest.mark.django_db
class TestRegisterEndpoint:
    @pytest.fixture(autouse=True)
    def setup_class(self, db):
        self.url = reverse("register")
        self.body = {
            "username": USER_USERNAME_1,
            "email": USER_EMAIL_1,
            "password": USER_PASSWORD_1,
        }

    def test_register_success(self, drf_client):
        response = drf_client.post(self.url, data=self.body, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert "password" not in response.data
        user = User.objects.get(username=USER_USERNAME_1)
        assert user.check_password(USER_PASSWORD_1)

    def test_register_fail_duplicate_username(self, drf_client, user_1):
        response = drf_client.post(self.url, data=self.body, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "username" in response.data

    def test_register_fail_duplicate_email(self, drf_client, user_1):
        self.body["username"] = USER_USERNAME_2
        response = drf_client.post(self.url, data=self.body, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in response.data
