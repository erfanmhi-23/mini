from django.shortcuts import render
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework import generics, permissions
from .models import Comment, Rating
from .serializers import CommentSerializer, RatingSerializer
from django.db.models import Avg


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

def broadcast_comment(comment):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"video_{comment.video.id}",
        {
            "type": "video_update",
            "data": {
                "video_id": comment.video.id,
                "comments_count": Comment.objects.filter(video=comment.video).count()
            }
        }
    )

def broadcast_rating(rating):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"video_{rating.video.id}",
        {
            "type": "video_update",
            "data": {
                "video_id": rating.video.id,
                "rating_avg": round(Rating.objects.filter(video=rating.video).aggregate(Avg('score'))['score__avg'] or 0, 2)
            }
        }
    )
