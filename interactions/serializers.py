from rest_framework import serializers
from .models import Comment, Rating

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'user', 'video', 'content', 'created_at')
        read_only_fields = ('created_at',)

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('id', 'user', 'video', 'score')
