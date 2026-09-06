from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import DestroyAPIView, ListCreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from books.models import Book
from config.pagination import ReviewCursorPagination
from .models import Review
from .permissions import IsOwner
from .serializers import ReviewSerializer


class ReviewListCreateView(ListCreateAPIView):
    serializer_class = ReviewSerializer
    pagination_class = ReviewCursorPagination

    def get_queryset(self):
        return (
            Review.objects.filter(
                book=get_object_or_404(
                    Book.objects.only("pk"), pk=self.kwargs["book_id"]
                )
            )
            .select_related("user")
            .order_by("-created_at", "-id")
        )

    def create(self, request, *args, **kwargs):
        book = get_object_or_404(
            Book.objects.only("pk"), pk=self.kwargs["book_id"]
        )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            with transaction.atomic():
                serializer.save(book=book, user=request.user)
        except IntegrityError as error:
            raise ValidationError({"detail": "you already reviewed this book"}) from error

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReviewUpdateDeleteView(UpdateAPIView, DestroyAPIView):
    queryset = Review.objects.select_related("user")
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsOwner]
