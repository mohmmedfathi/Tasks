from rest_framework.pagination import CursorPagination


class BookStoreCursorPagination(CursorPagination):
    page_size_query_param = 'limit'


class BookCursorPagination(BookStoreCursorPagination):
    ordering = ("title", "id")
