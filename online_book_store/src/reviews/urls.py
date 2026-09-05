from django.urls import path

from .api import ReviewListCreateView

urlpatterns = [
    path(
        "books/<int:book_id>/reviews/",
        ReviewListCreateView.as_view(),
        name="review-list",
    ),
]
