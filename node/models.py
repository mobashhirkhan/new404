from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.


class NodeManager(BaseUserManager):
    def create_node(self, username, password, origin):
        node = self.model(username=username, origin=origin)
        node.set_password(password)
        node.save(using=self._db)
        return node


class Node(AbstractBaseUser):
    #team_num = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    origin = models.URLField()
    
    objects = NodeManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

    def check_password(self, raw_password):
        # Implement password checking logic here
        # This is especially important if you want to use basic authentication
        # Example:
        return raw_password == self.password
