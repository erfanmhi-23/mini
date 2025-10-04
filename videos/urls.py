from django.urls import path
from .views import VideoCreateView, VideoListView, VideoDetailView

urlpatterns = [
    path('', VideoListView.as_view(), name='video-list'),
    path('create/', VideoCreateView.as_view(), name='video-create'),
    path('<int:pk>/', VideoDetailView.as_view(), name='video-detail'),
]
