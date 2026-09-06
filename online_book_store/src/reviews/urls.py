from django.urls import path

from .api import ReviewListCreateView, ReviewUpdateDeleteView

urlpatterns = [
    path(
        "books/<int:book_id>/reviews/",
        ReviewListCreateView.as_view(),
        name="review-list-create",
    ),
    path("reviews/<int:pk>/", ReviewUpdateDeleteView.as_view(), name="review-detail"),
]
