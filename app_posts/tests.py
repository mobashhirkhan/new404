from django.test import TestCase
from authors.models import Author, AuthorManager
from .models import AppPost
from .serializers import AppPostSerializer
from authors.serializers import AuthorSerializer

# Create your tests here.
class PostTestCase(TestCase):
    """ Test case for Post model"""
    def setUp(self):
        """ Set up for Post model test case"""
        self.author = Author.objects.create(username="Node-Netter#1")

        self.post = AppPost.objects.create(author = self.author,  
                                            title = "Test Post 1", 
                                            description = "Test Description 1", 
                                            source = "Test Source 1",  
                                            contentType = "plain", 
                                            content = "Test Content 1",  
                                            categories = 'Test Category 1, Test Category 2', 
                                            visibility = "PUBLIC", 
                                            unlisted = False)
        
    def test_post_creation(self):
        """ Test post creation"""
        post = AppPost.objects.get(id = self.post.id)
        self.assertEqual(post.title, "Test Post 1")
        self.assertEqual(post.author, self.author)
        self.assertEqual(post.description, "Test Description 1")
        self.assertEqual(post.source, "Test Source 1")
        self.assertEqual(post.categories, 'Test Category 1, Test Category 2')
        self.assertEqual(post.visibility, "PUBLIC")

    def test_post_str_method(self):
        """ Test post str method"""
        self.assertEqual(str(self.post), "Test Post 1 by Node-Netter#1")

    def test_post_serializer(self):
        """ Test post serializer"""
        post = AppPost.objects.get(id = self.post.id)
        serializer = AppPostSerializer(post)
        self.assertEqual(serializer.data['title'], "Test Post 1")
        self.assertEqual(serializer.data['author'], self.author.id)
        self.assertEqual(serializer.data['description'], "Test Description 1")
        self.assertEqual(serializer.data['source'], "Test Source 1")
        self.assertEqual(serializer.data['categories'], 'Test Category 1, Test Category 2')
        self.assertEqual(serializer.data['visibility'], "PUBLIC")
    
    def test_post_serializer_update(self):
        """ Test post serializer updatation, creation and deletion"""
        data = {'title': 'Test Post 2',
                'description': 'Test Description 2',
                'content': 'Test Content 2',
                'categories': 'Test Category 3, Test Category 4',
                'visibility': 'FRIENDS'}
        serializer = AppPostSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        serializer.save(author = self.author)
        post = AppPost.objects.get(title = 'Test Post 2')
        self.assertEqual(post.title, "Test Post 2")
        self.assertEqual(post.author, self.author)
        self.assertEqual(post.description, "Test Description 2")
        self.assertEqual(post.categories, 'Test Category 3, Test Category 4')
        self.assertEqual(post.content, 'Test Content 2')
        self.assertEqual(post.visibility, "FRIENDS")
        
        post.delete()
        self.assertEqual(AppPost.objects.filter(title = 'Test Post 2').count(), 0)
    
    def tearDown(self):
        """ Deletes all the objects created for the test case """
        self.author.delete()
        self.post.delete()