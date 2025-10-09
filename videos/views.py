from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from .models import Video
from .serializers import VideoSerializer
from users.models import Subscription
from rest_framework.decorators import api_view
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer



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
    
@api_view(['POST'])
def increment_view(request, video_id):
    video = Video.objects.get(id=video_id)
    video.views += 1
    video.save()

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"video_{video.id}",
        {
            "type": "video_update",
            "data": {
                "video_id": video.id,
                "views": video.views
            }
        }
    )
    return Response({"views": video.views})
