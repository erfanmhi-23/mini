from rest_framework import serializers
from .models import WatchHistory

class WatchHistorySerializer(serializers.ModelSerializer):
    class Meta :
        model = WatchHistory
        fields = ('id', 'user', 'video', 'watched_at', 'progress')
        read_only_fields = ('watched_at',)
        