from rest_framework import serializers

from .models import Author
from .models import FriendRequest



class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        # fields = "__all__"
        fields = ['type', 'id', 'url', 'host', 'displayName', 'github', 'profileImage']
        read_only_fields = ['type', 'id', 'url', 'host']


class FriendRequestSerializer(serializers.ModelSerializer):
    fromAuthor = AuthorSerializer()
    toAuthor = AuthorSerializer()
    class Meta:
        model = FriendRequest
        fields = ['type', 'id', 'origin', 'fromAuthor', 'toAuthor']
        read_only_fields = ['type', 'id']
