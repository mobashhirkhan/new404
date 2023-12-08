import uuid

from django.db import models
from django.utils import timezone

from app_posts.models import AppPost
from authors.models import Author

baseURL_host = "node-net-46d70235bc29.herokuapp.com"
baseURL = f"https://{baseURL_host}/api"


# "text/markdown" or text/plain
# Create your models here.
class Comment(models.Model):
    """Comment model"""

    type = models.CharField(max_length=200, default="Comment", editable=False)
    id = models.TextField(primary_key=True, default=uuid.uuid4, editable=False)
    id2 = models.TextField(null=True, editable=False)
    origin = models.TextField(blank=True, null=True)
    summary = models.CharField(max_length=255, default="")

    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)
    content_type = [
        ("plain", "plain"),
        ("markdown", "markdown"),
    ]
    contentType = models.CharField(
        max_length=20, choices=content_type, default=("plain", "plain")
    )
    content = (
        models.TextField()
    )  # storing both for easy reference, keep user input so is editable
    contentPlain = models.TextField(default="", editable=False)
    contentMarkdown = models.TextField(default="", editable=False)

    published = models.DateTimeField(
        default=timezone.now, editable=False
    )  # ISO 8601 TIMESTAMP "2015-03-09T13:07:04+00:00"
    post = models.ForeignKey(AppPost, on_delete=models.CASCADE, null=True)
    liked = models.ManyToManyField("likes.Like")

    def __str__(self):
        return self.type + " by " + self.author.username

    def save(self, *args, **kwargs):
        # Set default origin and source based on baseURL, author's ID, and post's ID
        if not self.id2:
            self.id2 = self.id
            self.id = f"{self.post.id}/comments/{self.id2}"
        if not self.origin:
            self.origin = self.id

        # Call the original save method
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-published"]

    """
        
    author_as_id = models.Foreignkey(Author, on_delete=models.CASCADE, editable=False)
    post_as_id = models.Foreignkey(Post, on_delete=models.CASCADE, editable=False)
    
    {
    "type":"comment",
    "author":{
        "type":"author",
        # ID of the Author (UUID)
        "id":"http://127.0.0.1:5454/authors/1d698d25ff008f7538453c120f581471",
        # url to the authors information
        "url":"http://127.0.0.1:5454/authors/1d698d25ff008f7538453c120f581471",
        "host":"http://127.0.0.1:5454/",
        "displayName":"Greg Johnson",
        # HATEOS url for Github API
        "github": "http://github.com/gjohnson",
        # Image from a public domain
        "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
    }
    "comment":"Sick Olde English",
    "contentType":"text/markdown",
    # ISO 8601 TIMESTAMP
    "published":"2015-03-09T13:07:04+00:00",
    # ID of the Comment (UUID)
    "id":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments/f6255bb01c648fe967714d52a89e8e9c",
}
    """
