from django.db.models import Avg, Count
from django.db.models.functions import Round
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from books.models import Book
from books.serializers import BookDetailSerializer, BookListSerializer
from config.pagination import BookCursorPagination


class BookListView(APIView):
    pagination_class = BookCursorPagination

    def get(self, request):
        books = (
            Book.objects.defer("content")
            .annotate(
                avg_rating=Round(Avg("reviews__rating"), 1),
                reviews_count=Count("reviews"),
            )
        )
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(books, request, view=self)

        serializer = BookListSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class BookDetailView(APIView):
    def get(self, request, pk):
        books = Book.objects.annotate(
            avg_rating=Round(Avg("reviews__rating"), 1),
            reviews_count=Count("reviews"),
        )
        book = get_object_or_404(books, pk=pk)
        return Response(BookDetailSerializer(book).data)
