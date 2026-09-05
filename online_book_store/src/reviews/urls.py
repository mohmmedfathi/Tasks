from django.urls import path

from .api import ReviewDetailView, ReviewListCreateView

urlpatterns = [
    path(
        "books/<int:book_id>/reviews/",
        ReviewListCreateView.as_view(),
        name="review-list",
    ),
    path(
        "reviews/<int:pk>/",
        ReviewDetailView.as_view(
            {"put": "update", "patch": "partial_update", "delete": "destroy"}
        ),
        name="review-detail",
    ),
]
