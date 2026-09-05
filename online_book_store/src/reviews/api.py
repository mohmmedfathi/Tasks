from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from books.models import Book
from config.pagination import ReviewCursorPagination
from .models import Review
from .serializers import ReviewSerializer


class ReviewListCreateView(APIView):
    pagination_class = ReviewCursorPagination

    def get(self, request, book_id):
        get_object_or_404(Book.objects.only("pk"), pk=book_id)
        reviews = (
            Review.objects.filter(book_id=book_id)
            .select_related("user")
            .order_by("-created_at", "-id")
        )

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(reviews, request, view=self)
        serializer = ReviewSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, book_id):
        book = get_object_or_404(Book.objects.only("pk"), pk=book_id)
        serializer = ReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            with transaction.atomic():
                serializer.save(book=book, user=request.user)
        except IntegrityError:
            raise ValidationError({"detail": "you already reviewed this book"})

        return Response(serializer.data, status=status.HTTP_201_CREATED)
