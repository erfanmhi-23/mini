from django.shortcuts import render

from rest_framework import generics, permissions
from .models import Comment, Rating
from .serializers import CommentSerializer, RatingSerializer

class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        video_id = self.kwargs['video_id']
        return Comment.objects.filter(video__id=video_id)

class RatingCreateUpdateView(generics.CreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]
