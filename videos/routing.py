from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/videos/(?P<video_id>\d+)/$', consumers.VideoConsumer.as_asgi()),
]
