from rest_framework import serializers

from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    # only the username of other users leaves the api
    username = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Review
        exclude = ["book"]
        read_only_fields = ["user"]
