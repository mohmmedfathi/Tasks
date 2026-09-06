import pytest
from django.urls import reverse
from rest_framework import status

from books.models import Book
from reviews.models import Review
from tests.constants import (
    BOOK_DETAIL_FIELDS,
    FIXTURE_BOOKS_COUNT,
    REVIEW_RATING_1,
    REVIEW_RATING_2,
    REVIEW_TEXT_1,
    REVIEW_TEXT_2,
)


@pytest.mark.django_db
class TestBookEndpoints:
    @pytest.fixture(autouse=True)
    def setup_class(self, db):
        self.book = Book.objects.get(pk=1)
        self.url_list = reverse("book-list")
        self.url_detail = reverse("book-detail", kwargs={"pk": self.book.pk})

    def test_get_books_list_success(self, authenticate_user_1, drf_client):
        response = drf_client.get(self.url_list)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == FIXTURE_BOOKS_COUNT

    def test_get_book_detail_success(self, authenticate_user_1, drf_client):
        response = drf_client.get(self.url_detail)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["content"] == self.book.content
        assert set(response.data) == BOOK_DETAIL_FIELDS

    def test_get_book_rating_statistics_success(
        self, authenticate_user_1, drf_client, user_1, user_2
    ):
        Review.objects.create(
            book=self.book, user=user_1, rating=REVIEW_RATING_1, text=REVIEW_TEXT_1
        )
        Review.objects.create(
            book=self.book, user=user_2, rating=REVIEW_RATING_2, text=REVIEW_TEXT_2
        )
        response = drf_client.get(self.url_detail)
        assert response.data["avg_rating"] == 4.5
        assert response.data["reviews_count"] == 2

    def test_get_book_without_reviews_has_no_rating_success(self, authenticate_user_1, drf_client):
        response = drf_client.get(self.url_detail)
        assert response.data["avg_rating"] is None
        assert response.data["reviews_count"] == 0
