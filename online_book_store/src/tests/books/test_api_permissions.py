import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestBookPermissions:
    @pytest.fixture(autouse=True)
    def setup_class(self, db):
        self.url_list = reverse("book-list")
        self.url_detail = reverse("book-detail", kwargs={"pk": 1})

    def test_get_books_fail_unauthenticated(self, drf_client):
        assert drf_client.get(self.url_list).status_code == status.HTTP_401_UNAUTHORIZED
        assert drf_client.get(self.url_detail).status_code == status.HTTP_401_UNAUTHORIZED
