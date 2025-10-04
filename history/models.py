from django.db import models
from users.models import CustomUser
from videos.models import Video

class WatchHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='watch_history')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='watch_history')
    watched_at = models.DateTimeField(auto_now_add=True)
    progress = models.IntegerField(default=0, help_text="Progress in percent")

    def __str__(self):
        return f"{self.user.username} watched {self.video.title}"