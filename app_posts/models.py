import uuid

from django.db import models
from django.utils import timezone

from authors.models import Author

baseURL_host = "node-net-46d70235bc29.herokuapp.com"
baseURL = f"https://{baseURL_host}/api"


# Create your models here.
class AppPost(models.Model):
    type = models.CharField(max_length=200, default="Post", editable=False)
    id = models.TextField(primary_key=True, default=uuid.uuid4, editable=False)
    id2 = models.TextField(null=True, editable=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()

    source = models.TextField(blank=True, null=True)
    origin = models.TextField(blank=True, null=True)

    content_type = [
        ("plain", "plain"),
        ("markdown", "markdown"),
        ("hyperlink", "hyperlink"),
        ("image/png;base64", "image/png;base64"),
        ("image/jpeg;base64", "image/jpeg;base64"),
    ]

    contentType = models.CharField(
        max_length=20, choices=content_type, default=("plain", "plain")
    )
    content = (
        models.TextField()
    )  # storing both for easy reference, keep user input so is editable
    contentPlain = models.TextField(default="", editable=False)
    contentMarkdown = models.TextField(default="", editable=False)

    count = models.IntegerField(default=0)
    categories = models.CharField(max_length=255, default="")
    published = models.DateTimeField(default=timezone.now, editable=False)
    visibility = models.CharField(
        max_length=10,
        choices=[("PUBLIC", "PUBLIC"), ("FRIENDS", "FRIENDS"), ("PRIVATE", "PRIVATE")],
        default=("PUBLIC", "PUBLIC"),
    )
    unlisted = models.BooleanField(default=False, editable=True)

    image = models.ImageField(null=True, blank=True, upload_to="post_images/")
    liked = models.ManyToManyField("likes.Like")
    comments = models.TextField(blank=True, null=True)

    friends_to_notify = models.ManyToManyField(
        Author, related_name="private_message", blank=True
    )

    # commentSrc is OPTIONAL

    def __str__(self):
        return self.title + " by " + self.author.username

    def save(self, *args, **kwargs):
        # Set default origin and source based on baseURL, author's ID, and post's ID
        if not self.id2:
            self.id2 = self.id
            self.id = f"{self.author.id}/posts/{self.id2}"
        if not self.origin:
            self.origin = self.id

        if not self.source:
            self.source = self.id

        if not self.comments:
            self.comments = f"{self.id}/comments"

        # Call the original save method
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-published"]
