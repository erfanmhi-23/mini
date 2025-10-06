from django.urls import path
from .views import WatchHistoryCreateView, WatchHistoryListView

urlpatterns = [
    path('create/', WatchHistoryCreateView.as_view(), name='watchhistory-create'),
    path('my/', WatchHistoryListView.as_view(), name='watchhistory-list'),
]
