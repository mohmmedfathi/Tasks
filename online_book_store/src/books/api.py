from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Book
from .serializers import BookDetailSerializer, BookListSerializer


class BookListView(APIView):
    def get(self, request):
        # content is the heavy column and the list never shows it
        books = Book.objects.defer("content").order_by("title")
        return Response(BookListSerializer(books, many=True).data)


class BookDetailView(APIView):
    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        return Response(BookDetailSerializer(book).data)
