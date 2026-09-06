import pytest
from django.urls import reverse
from rest_framework import status

from books.models import Book
from reviews.models import Review
from tests.constants import (
    MISSING_ID,
    REVIEW_FIELDS,
    REVIEW_RATING_1,
    REVIEW_RATING_2,
    REVIEW_RATING_ABOVE_MAX,
    REVIEW_TEXT_1,
    REVIEW_TEXT_2,
    USER_USERNAME_1,
    USER_USERNAME_2,
)


@pytest.mark.django_db
class TestReviewEndpoints:

    @pytest.fixture(autouse=True)
    def setup_class(self, db):
        self.book = Book.objects.get(pk=1)
        self.other_book = Book.objects.get(pk=2)
        self.url = reverse("review-list-create", kwargs={"book_id": self.book.pk})
        self.body = {"rating": REVIEW_RATING_1, "text": REVIEW_TEXT_1}

    def test_create_review_success(self, authenticate_user_1, drf_client, user_1):
        response = drf_client.post(self.url, data=self.body, format="json")

        assert response.status_code == status.HTTP_201_CREATED

        review = Review.objects.get()

        assert review.user == user_1
        assert review.book == self.book
        assert response.data["username"] == USER_USERNAME_1

    def test_create_review_fail_duplicate(self, authenticate_user_1, drf_client):
        drf_client.post(self.url, data=self.body, format="json")
        response = drf_client.post(self.url, data=self.body, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert Review.objects.count() == 1

    def test_create_review_fail_invalid_rating(self, authenticate_user_1, drf_client):
        self.body["rating"] = REVIEW_RATING_ABOVE_MAX

        response = drf_client.post(self.url, data=self.body, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "rating" in response.data

    def test_create_review_fail_book_not_found(self, authenticate_user_1, drf_client):
        url = reverse("review-list-create", kwargs={"book_id": MISSING_ID})

        response = drf_client.post(url, data=self.body, format="json")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_create_review_ignores_user_and_book_in_body_success(
        self, authenticate_user_1, drf_client, user_1, user_2
    ):
        # ensure a user cannot create a review as another user
        self.body["user"] = user_2.pk
        self.body["book"] = self.other_book.pk

        drf_client.post(self.url, data=self.body, format="json")

        review = Review.objects.get()

        assert review.user == user_1
        assert review.book == self.book

    def test_get_reviews_list_only_this_book_success(
        self, authenticate_user_1, drf_client, user_1, user_2
    ):
        review = Review.objects.create(
            book=self.book, user=user_1, rating=REVIEW_RATING_1, text=REVIEW_TEXT_1
        )

        Review.objects.create(
            book=self.other_book, user=user_2, rating=REVIEW_RATING_1, text=REVIEW_TEXT_1
        )

        response = drf_client.get(self.url)

        assert [r["id"] for r in response.data["results"]] == [review.pk]

    def test_get_reviews_list_newest_first_with_author_success(
        self, authenticate_user_1, drf_client, user_1, user_2
    ):
        older = Review.objects.create(
            book=self.book, user=user_1, rating=REVIEW_RATING_1, text=REVIEW_TEXT_1
        )

        newer = Review.objects.create(
            book=self.book, user=user_2, rating=REVIEW_RATING_2, text=REVIEW_TEXT_2
        )

        response = drf_client.get(self.url)

        assert response.status_code == status.HTTP_200_OK

        results = response.data["results"]

        assert [review["id"] for review in results] == [newer.pk, older.pk]
        assert set(results[0]) == REVIEW_FIELDS
        assert results[0]["username"] == USER_USERNAME_2

    def test_update_review_success(self, authenticate_user_1, drf_client, user_1):
        review = Review.objects.create(
            book=self.book, user=user_1, rating=REVIEW_RATING_1, text=REVIEW_TEXT_1
        )

        url = reverse("review-detail", kwargs={"pk": review.pk})

        response = drf_client.patch(url, data={"rating": REVIEW_RATING_2}, format="json")

        assert response.status_code == status.HTTP_200_OK

        review.refresh_from_db()

        assert review.rating == REVIEW_RATING_2

    def test_update_review_ignores_owner_in_body_success(
        self, authenticate_user_1, drf_client, user_1, user_2
    ):
        # ensure a user cannot transfer review ownership to another user
        review = Review.objects.create(
            book=self.book, user=user_1, rating=REVIEW_RATING_1, text=REVIEW_TEXT_1
        )

        url = reverse("review-detail", kwargs={"pk": review.pk})

        drf_client.patch(url, data={"user": user_2.pk, "rating": REVIEW_RATING_2}, format="json")

        review.refresh_from_db()

        assert review.user == user_1

    def test_delete_review_success(self, authenticate_user_1, drf_client, user_1):
        review = Review.objects.create(
            book=self.book, user=user_1, rating=REVIEW_RATING_1, text=REVIEW_TEXT_1
        )

        url = reverse("review-detail", kwargs={"pk": review.pk})

        response = drf_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Review.objects.filter(pk=review.pk).exists()