from django.test import TestCase
# importing author
from authors.models import Author
from authors.models import AuthorManager
from authors.serializers import AuthorSerializer
import uuid

class AuthorModelTest(TestCase):
    # setting up authors
    def setUp(self):
        self.author1 = Author.objects.create(username="testuser")
        self.author2 = Author.objects.create(username="testuser2")

        self.serializer1 = AuthorSerializer(self.author1)
        self.serializer2 = AuthorSerializer(self.author2)

    # checking if name is set to username
    def set_to_username(self):
        self.assertEqual(self.author1.username, "testuser")

    # checking if author is not empty
    def test_id_is_not_none(self):
        self.assertIsNotNone(self.author1.id)

    # checking if author ids are unique
    def test_ids_are_unique(self):
        self.assertNotEqual(self.author1.id, self.author2.id)

    # testing from serializer
    def test_author_fields_values(self):
        data = self.serializer1.data
        self.assertEqual(data['username'], 'testuser')
