from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post, Like
from user_notifications.models import Notification
from django.contrib.contenttypes.models import ContentType

class LikePostAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

        like, created = Like.objects.get_or_create(post=post, user=request.user)
        if not created:
            return Response({"detail": "Already liked"}, status=status.HTTP_400_BAD_REQUEST)

        # Create notification for the post author if not liking own post
        if post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb="liked your post",
                target=post
            )

        return Response({"detail": "Post liked"}, status=status.HTTP_200_OK)


class UnlikePostAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

        like = Like.objects.filter(post=post, user=request.user)
        if like.exists():
            like.delete()
            return Response({"detail": "Post unliked"}, status=status.HTTP_200_OK)
        return Response({"detail": "You have not liked this post"}, status=status.HTTP_400_BAD_REQUEST)
