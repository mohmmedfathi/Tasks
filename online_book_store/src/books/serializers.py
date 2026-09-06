from rest_framework import serializers

from books.models import Book


class BookListSerializer(serializers.ModelSerializer):
    avg_rating = serializers.FloatField(read_only=True)
    reviews_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Book
        fields = ["id", "title", "author", "description", "avg_rating", "reviews_count"]


class BookDetailSerializer(BookListSerializer):
    class Meta(BookListSerializer.Meta):
        fields = BookListSerializer.Meta.fields + [
            "published_date",
            "content",
        ]
