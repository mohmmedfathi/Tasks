import pytest
from django.urls import reverse
from rest_framework import status

from books.models import Book
from reviews.models import Review
from tests.constants import REVIEW_RATING_1, REVIEW_RATING_2, REVIEW_TEXT_1, REVIEW_TEXT_2


@pytest.mark.django_db
class TestReviewPermissions:
    @pytest.fixture(autouse=True)
    def setup_class(self, db, user_1):
        self.book = Book.objects.get(pk=1)
        self.review = Review.objects.create(
            book=self.book, user=user_1, rating=REVIEW_RATING_1, text=REVIEW_TEXT_1
        )
        self.url = reverse("review-list-create", kwargs={"book_id": self.book.pk})
        self.url_detail = reverse("review-detail", kwargs={"pk": self.review.pk})
        self.body = {"rating": REVIEW_RATING_2, "text": REVIEW_TEXT_2}

    def test_review_endpoints_fail_unauthenticated(self, drf_client):
        listed = drf_client.get(self.url)
        created = drf_client.post(self.url, data=self.body, format="json")
        patched = drf_client.patch(self.url_detail, data=self.body, format="json")
        deleted = drf_client.delete(self.url_detail)
        assert listed.status_code == status.HTTP_401_UNAUTHORIZED
        assert created.status_code == status.HTTP_401_UNAUTHORIZED
        assert patched.status_code == status.HTTP_401_UNAUTHORIZED
        assert deleted.status_code == status.HTTP_401_UNAUTHORIZED

    def test_other_user_cannot_update_or_delete_review(self, authenticate_user_2, drf_client):
        # ensure authorization prevents users from modifying reviews they do not own
        patched = drf_client.patch(self.url_detail, data=self.body, format="json")
        deleted = drf_client.delete(self.url_detail)
        assert patched.status_code == status.HTTP_403_FORBIDDEN
        assert deleted.status_code == status.HTTP_403_FORBIDDEN
        self.review.refresh_from_db()
        assert self.review.rating == REVIEW_RATING_1
