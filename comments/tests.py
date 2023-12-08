# Create your tests here.
from django.test import TestCase

from authors.models import Author, AuthorManager

from .models import AppPost, Comment
from .serialisers import CommentSerializer

# Create your tests here.


class CommentTest(TestCase):
    """Test case for Comment model"""

    def setUp(self):
        """Set up for Comment model test case"""
        # create an author
        self.author = Author.objects.create(username="Node-Netter#1")
        # create a post
        self.post = AppPost.objects.create(
            author=self.author,
            title="Test Post 1",
            description="Test Description 1",
            source="Test Source 1",
            contentType="plain",
            content="Test Content 1",
            categories="Test Category 1, Test Category 2",
            visibility="PUBLIC",
            unlisted=False,
        )
        # create a comment
        self.comment = Comment.objects.create(
            author=self.author,
            post=self.post,
            content="Test Comment 1",
            contentType="plain",
        )

    def test_comment_creation(self):
        """Test comment creation"""
        comment = Comment.objects.get(content="Test Comment 1")
        self.assertEqual(comment.content, "Test Comment 1")
        self.assertEqual(comment.author, self.author)
        self.assertEqual(str(comment.post), str(self.post))
        self.assertEqual(comment.contentType, "plain")

    def test_comment_serializer(self):
        """Test comment serializer"""
        comment = Comment.objects.get(content="Test Comment 1")
        serializer = CommentSerializer(comment)
        self.assertEqual(serializer.data["content"], "Test Comment 1")
        self.assertEqual(serializer.data["author"], self.author.id)
        self.assertEqual(serializer.data["post"], str(self.post.id))
        self.assertEqual(serializer.data["contentType"], "plain")

    def tearDown(self):
        """Tear down for Comment model test case"""
        self.author.delete()
        self.post.delete()
        self.comment.delete()
