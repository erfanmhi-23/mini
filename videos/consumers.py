import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

class VideoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.video_id = self.scope['url_route']['kwargs']['video_id']
        self.group_name = f"video_{self.video_id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        await self.send_current_state()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_current_state(self):
        video_data = await sync_to_async(self.get_video_data)()
        await self.send(text_data=json.dumps(video_data))

    def get_video_data(self):
        from videos.models import Video
        from interactions.models import Comment, Rating
        from django.db.models import Avg
        video = Video.objects.get(id=self.video_id)
        comments_count = Comment.objects.filter(video=video).count()
        rating_avg = Rating.objects.filter(video=video).aggregate(Avg('score'))['score__avg'] or 0
        return {
            "video_id": video.id,
            "title": video.title,
            "views": video.views,
            "comments_count": comments_count,
            "rating_avg": round(rating_avg, 2)
        }

    async def video_update(self, event):
        await self.send(text_data=json.dumps(event['data']))
