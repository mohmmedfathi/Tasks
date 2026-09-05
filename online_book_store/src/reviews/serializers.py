from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Review


# username only so nothing else about other users leaves the api
class ReviewAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "username"]


class ReviewSerializer(serializers.ModelSerializer):
    user = ReviewAuthorSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ["id", "user", "rating", "text", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
