import pytest
from django.core.management import call_command
from rest_framework.test import APIClient

from tests.constants import (
    FIXTURES,
    USER_EMAIL_1,
    USER_EMAIL_2,
    USER_PASSWORD_1,
    USER_PASSWORD_2,
    USER_USERNAME_1,
    USER_USERNAME_2,
)
from users.models import User


# load books into test database once per test session
@pytest.fixture(scope="session", autouse=True)
def load_books(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("loaddata", *FIXTURES)


@pytest.fixture
def drf_client():
    return APIClient()


@pytest.fixture
def user_1(db):
    return User.objects.create_user(
        username=USER_USERNAME_1, email=USER_EMAIL_1, password=USER_PASSWORD_1
    )


@pytest.fixture
def user_2(db):
    return User.objects.create_user(
        username=USER_USERNAME_2, email=USER_EMAIL_2, password=USER_PASSWORD_2
    )


@pytest.fixture
def authenticate_user_1(drf_client, user_1):
    drf_client.force_authenticate(user_1)


@pytest.fixture
def authenticate_user_2(drf_client, user_2):
    drf_client.force_authenticate(user_2)
