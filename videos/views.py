from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Video
from .serializers import VideoSerializer


class VideoCreateView(generics.CreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAdminUser]

class VideoListView(generics.ListAPIView):
    queryset = Video.objects.filter(active=True)
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticated]

class VideoDetailView(generics.RetrieveAPIView):
    queryset = Video.objects.filter(active=True)
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticated]
