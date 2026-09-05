from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Book
from .serializers import BookDetailSerializer, BookListSerializer
from config.pagination import BookCursorPagination


class BookListView(APIView):
    pagination_class = BookCursorPagination

    def get(self, request):
        # content is the heavy column and the list never shows it
        books = Book.objects.defer("content").order_by("title")
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(books, request, view=self)

        serializer = BookListSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class BookDetailView(APIView):
    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        return Response(BookDetailSerializer(book).data)
