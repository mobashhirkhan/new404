import uuid

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

baseURL_host = "connection-net-e444016a9ef0.herokuapp.com"
baseURL = f"https://{baseURL_host}/api"


# custom class to manage our custom Author
class AuthorManager(BaseUserManager):
    """Custom manager for our custom Author"""

    def create_user(
        self, username="Node-Netter#1", email=None, password=None, **extra_fields
    ):
        """Create and save a user with the given username, email, and password."""
        extra_fields.setdefault("is_active", False)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("displayName", username)  # Set displayName to username
        extra_fields.setdefault("host", baseURL_host)

        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        extra_fields.setdefault("url", f"{baseURL}/authors/{str(user.id)}")
        extra_fields.setdefault("origin", extra_fields["url"])
        extra_fields.setdefault("source", extra_fields["url"])
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        """Create and save a superuser with the given username, email, and password."""
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(username, email, password, **extra_fields)

    # needed solely because we may need to compare authors and their posts. but not used yet
    def getAuthor(self):
        """Get the author"""
        return self


# Create your models here.
class Author(AbstractUser):
    """Custom Author class that extends the AbstractUser class"""

    id = models.TextField(primary_key=True, default=uuid.uuid4, editable=False)
    id2 = models.TextField(null=True, editable=False)
    # #base class already has id and was clashing, will need to know how to use later
    type = models.CharField(max_length=200, default="Author", editable=False)
    host = models.TextField(blank=True, null=True)
    origin = models.TextField(blank=True, null=True)

    displayName = models.CharField(
        max_length=255, blank=True, null=True
    )  # will set to username(just use username)
    url = models.TextField(blank=True, null=True)
    github = models.TextField(blank=True, null=True)
    # profileImage = models.ImageField() for later
    followers = models.ManyToManyField(
        "self", blank=True, symmetrical=False, related_name="they_follow_me"
    )
    # my_posts = models.ManyToManyField(
    #     "app_posts.AppPost", blank=True, related_name="posts_i_see"
    # )

    following = models.ManyToManyField(
        "self", blank=True, symmetrical=False, related_name="i_follow_them"
    )  # the authors i'm following
    friends = models.ManyToManyField(
        "self", blank=True, symmetrical=True
    )  # we follow each other

    foreign_authors = models.JSONField(blank=True, null=True)
    profileImage = models.ImageField(null=True, blank=True, upload_to='author_images/')

    # auth, need a custom manager because we have a custom author
    objects = AuthorManager()

    # def __str__(self): was getting error for comparing authors and users so commented out for now
    #     return f"The user is {self.username} with GitHub {self.github}"
    #
    # def get_my_posts(self):
    #     return self.my_posts.all()

    # all users will have an inbox so create inbox when user created
    def save(self, *args, **kwargs):
        if not self.displayName:
            self.displayName = self.username
        if not self.host:
            self.host = baseURL_host
        if not self.url:
            self.url = f"{baseURL}/authors/{str(self.id)}"
            self.origin = self.url
            self.source = self.url

        if not self.id2:
            self.id2 = self.id
            self.id = self.url
        super().save(*args, **kwargs)

        from inboxes.models import Inbox

        Inbox.objects.get_or_create(author=self)


# friend request object
class FriendRequest(models.Model):
    type = models.CharField(max_length=100, default="Request", editable=False)
    id = models.TextField(primary_key=True, default=uuid.uuid4, editable=False)
    id2 = models.TextField(null=True, editable=False)
    origin = models.TextField(blank=True, null=True)

    fromAuthor = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="fromUser"
    )
    toAuthor = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="toUser"
    )

    def save(self, *args, **kwargs):
        # Set default origin and source based on baseURL, author's ID, and post's ID
        if not self.id2:
            self.id2 = self.id
            self.id = f"{baseURL}/authors/{self.toAuthor}/followers/{self.fromAuthor}"
        if not self.origin:
            self.origin = f"{str(self.toAuthor.id)}/inbox/{str(self.fromAuthor.id2)}"


        # Call the original save method
        super().save(*args, **kwargs)
