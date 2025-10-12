from django.urls import path
from .views import LikePostAPIView, UnlikePostAPIView

urlpatterns = [
    path('<int:pk>/like/', LikePostAPIView.as_view(), name='like-post'),
    path('<int:pk>/unlike/', UnlikePostAPIView.as_view(), name='unlike-post'),
]
