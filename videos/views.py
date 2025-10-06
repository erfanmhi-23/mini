from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from .models import Video
from .serializers import VideoSerializer
from users.models import Subscription


class VideoCreateView(generics.CreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAdminUser]

class VideoListView(generics.ListAPIView):
    queryset = Video.objects.filter(active=True)
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticated]

class VideoDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            video = Video.objects.get(pk=pk, active=True)
        except Video.DoesNotExist:
            return Response({"detail": "Video not found."}, status=404)

        today = timezone.localdate()
        subscription = Subscription.objects.filter(user=request.user, end_date__gte=today).order_by('-start_date').first()
        can_watch = bool(subscription)

        data = {
            "id": video.id,
            "title": video.title,
            "description": video.description,
            "duration": video.duration,
            "upload": video.upload,
            "can_watch": can_watch
        }

        return Response(data, status=200)
