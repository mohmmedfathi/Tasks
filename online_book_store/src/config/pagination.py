from rest_framework.pagination import CursorPagination


class BookStoreCursorPagination(CursorPagination):
    page_size_query_param = 'limit'
    max_page_size = 100 # cap so one request never pull the whole table


class BookCursorPagination(BookStoreCursorPagination):
    ordering = ("title", "id")


class ReviewCursorPagination(BookStoreCursorPagination):
    ordering = ("-created_at", "-id")
