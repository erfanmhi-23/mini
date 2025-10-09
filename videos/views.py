from rest_framework import generics, permissions, status
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
    #permission_classes = [permissions.IsAuthenticated]

class VideoDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            video = Video.objects.get(pk=pk, active=True)
        except Video.DoesNotExist:
            return Response({"detail": "Video not found."}, status=status.HTTP_404_NOT_FOUND)

        today = timezone.localdate()
        subscription = Subscription.objects.filter(
            user=request.user, active=True, end_date__gte=today
        ).order_by('-start_date').first()

        if not subscription:
            return Response({"detail": "No active subscription found."}, status=status.HTTP_403_FORBIDDEN)

        data = {
            "id": video.id,
            "title": video.title,
            "description": video.description,
            "duration": video.duration,
            "upload": video.upload,
        }

        return Response(data, status=status.HTTP_200_OK)