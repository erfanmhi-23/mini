from django.db import models
from users.models import CustomUser

class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    file_url = models.URLField()
    upload_date = models.DateTimeField(auto_now_add=True)
    duration = models.IntegerField(help_text="Duration in seconds")
    active = models.BooleanField(default=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title