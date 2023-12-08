from rest_framework import serializers

from app_posts.serializers import AppPostSerializer
from authors.serializers import FriendRequestSerializer
from comments.serialisers import CommentSerializer
from likes.serializers import LikeSerializer
from .models import Inbox


class InboxSerializer(serializers.ModelSerializer):
    posts = AppPostSerializer(many=True, read_only=True)
    friend_requests = FriendRequestSerializer(many=True, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Inbox
        fields = ['type', 'posts', 'friend_requests', 'likes', 'comments']
