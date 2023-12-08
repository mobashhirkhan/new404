from django.contrib.auth.backends import BaseBackend
from .models import Node


class NodeBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        print("authenticating...")
        try:
            node = Node.objects.get(username=username)
        except Node.DoesNotExist:
            return None

        if node.check_password(password):
            return node

    def get_user(self, user_id):
        try:
            return Node.objects.get(pk=user_id)
        except Node.DoesNotExist:
            return None