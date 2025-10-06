from django.shortcuts import render

from rest_framework import generics, permissions
from .models import WatchHistory
from .serializers import WatchHistorySerializer

class WatchHistoryCreateView(generics.CreateAPIView):
    queryset = WatchHistory.objects.all()
    serializer_class = WatchHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

class WatchHistoryListView(generics.ListAPIView):
    serializer_class = WatchHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WatchHistory.objects.filter(user=self.request.user)
