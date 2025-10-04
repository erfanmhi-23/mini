from rest_framework import serializers
from .models import Video

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ('id', 'title', 'description', 'file_url', 'upload_date', 'duration', 'active')
        read_only_fields = ('upload_date',)
