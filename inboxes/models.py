from django.db import models

baseURL_host = "node-net-46d70235bc29.herokuapp.com"
baseURL = f"https://{baseURL_host}/api"

# Create your models here.
class Inbox(models.Model):
    type = models.CharField(max_length=200, default="Inbox", editable=False)
    author = models.OneToOneField(
        "authors.Author",
        on_delete=models.CASCADE,
        related_name="Owner",
        primary_key=True,
    )
    posts = models.JSONField(blank=True, null=True)
    friend_requests = models.JSONField(blank=True, null=True)
    likes = models.JSONField(blank=True, null=True)
    comments = models.JSONField(blank=True, null=True)

    def __str__(self):
        # return f"Author: {self.author} and items: {self.items}"
        return self.author.username + "'s inbox"

    # init to empty so dont get NoneType errors
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.posts = self.posts or []
        self.friend_requests = self.friend_requests or []
        self.likes = self.likes or []
        self.comments = self.comments or []
