from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'product', 'user', 'user_name', 'rating', 'title', 'body', 'created_at']
        read_only_fields = ['user', 'created_at']