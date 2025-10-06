from django.urls import path
from .views import CommentCreateView, CommentListView, RatingCreateUpdateView

urlpatterns = [
    path('comment/', CommentCreateView.as_view(), name='comment-create'),
    path('comment/<int:video_id>/', CommentListView.as_view(), name='comment-list'),
    path('rating/', RatingCreateUpdateView.as_view(), name='rating-create'),
]
