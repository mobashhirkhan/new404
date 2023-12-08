import uuid

from django.db import models
from django.utils import timezone
from authors.models import Author

baseURL_host = "node-net-46d70235bc29.herokuapp.com"
baseURL = f"https://{baseURL_host}/api"


# Create your models here.
class Like(models.Model):

    # OBJECT_TYPE = (
    #     ('post', 'post'),
    #     ('comment', 'comment')
    # )
    type = models.CharField(max_length=200,default="Like", editable=False)
    id = models.TextField(primary_key=True, default=uuid.uuid4, editable=False)
    id2 = models.TextField(null=True, editable=False)
    origin = models.TextField(blank=True, null=True)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    summary = models.CharField(max_length=255, default="")
    object_on = models.TextField() # post_id or post_id/comments/comment_id
    # object_type = models.CharField(max_length=255, choices=OBJECT_TYPE, default=('post', 'post'))
    # #no longer giving them option but setting manually
    object_type = models.CharField(max_length=255, default='post')
    published = models.DateTimeField(default=timezone.now,editable=False)

    def get_id(self):
        return self.id
    
    def get_summary(self):
        return self.author + "Likes your" + self.summary

    def save(self, *args, **kwargs):
        # Set default origin and source based on baseURL, author's ID, and post's ID
        if not self.id:
            self.id2 = self.id
            self.id = f"{self.object_on}/likes/{self.id2}"

        if not self.origin:
            self.origin = self.id


        # Call the original save method
        super().save(*args, **kwargs)
    
    def __str__(self):
        return "liked by " + self.author.username