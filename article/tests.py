from django.test import TestCase
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from article.models import Article
from product.models import Product
from django.utils import timezone


from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from article.models import Article
from product.models import Product
from django.utils import timezone

class ArticleModelTestCase(TestCase):
    def setUp(self):
        # Create a test user and a test article
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.product = Product.objects.create(name='Test Product')
        self.article = Article.objects.create(
            user=self.user,
            ride=self.product,
            title='Test Article',
            content='This is a test article content.',
            image='https://example.com/image.jpg',
            comments=[]
        )

    def test_add_comment(self):
        """Test that a comment is correctly added to the article."""
        self.article.add_comment(self.user, 'This is a test comment.')
        self.article.refresh_from_db()  # Refresh to get the latest data from the database
        self.assertEqual(len(self.article.comments), 1)
        self.assertEqual(self.article.comments[0]['content'], 'This is a test comment.')
        self.assertEqual(self.article.comments[0]['user'], self.user.username)

    def test_delete_comment(self):
        """Test that a comment can be correctly deleted by index."""
        self.article.add_comment(self.user, 'First Comment')
        self.article.add_comment(self.user, 'Second Comment')
        self.article.delete_comment(0)
        self.article.refresh_from_db()  # Refresh to get the latest data from the database
        self.assertEqual(len(self.article.comments), 1)
        self.assertEqual(self.article.comments[0]['content'], 'Second Comment')


class ArticleViewTestCase(TestCase):
    def setUp(self):
        # Create test users, article, and client for authentication
        self.client = Client()
        self.admin_user = User.objects.create_user(username='admin', password='adminpass')
        self.regular_user = User.objects.create_user(username='user', password='userpass')
        
        # Assign a user profile with admin privileges
        self.admin_user.userprofile.privilege = 'admin'
        self.admin_user.userprofile.save()
        
        self.product = Product.objects.create(name='Test Product')
        self.article = Article.objects.create(
            user=self.admin_user,
            ride=self.product,
            title='Test Article',
            content='Test content for article',
            image='https://example.com/image.jpg',
            comments=[]
        )

    def test_create_article(self):
        """Test creating an article with valid data."""
        self.client.login(username='admin', password='adminpass')
        response = self.client.post(reverse('article:make_article_form'), {
            'title': 'New Article',
            'content': 'New article content',
        })
        self.assertEqual(response.status_code, 302)  # Check for redirect after successful post
        self.assertTrue(Article.objects.filter(title='New Article').exists())

    def test_add_comment_to_article(self):
        """Test adding a comment to an article as an authenticated user."""
        self.client.login(username='user', password='userpass')
        response = self.client.post(
            reverse('article:add_comment', args=[self.article.id]),
            {'comment_text': 'This is a new comment'}
        )
        self.assertEqual(response.status_code, 200)
        self.article.refresh_from_db()
        self.assertTrue(len(self.article.comments) > 0)
        self.assertEqual(self.article.comments[0]['content'], 'This is a new comment')

    def test_delete_comment(self):
        """Test deleting a comment as an admin user."""
        self.article.add_comment(self.regular_user, 'Comment to be deleted')
        self.client.login(username='admin', password='adminpass')
        
        response = self.client.post(
            reverse('article:delete_comment', args=[self.article.id, 0])
        )
        self.assertEqual(response.status_code, 200)
        self.article.refresh_from_db()
        self.assertEqual(len(self.article.comments), 0)

    def test_edit_article(self):
        """Test editing an existing article's title and content."""
        self.client.login(username='admin', password='adminpass')
        response = self.client.post(
            reverse('article:edit_article', args=[self.article.id]),
            {'title': 'Updated Article', 'content': 'Updated content'}
        )
        self.article.refresh_from_db()
        self.assertEqual(self.article.title, 'Updated Article')
        self.assertEqual(self.article.content, 'Updated content')

    def test_delete_article(self):
        """Test deleting an article as an admin."""
        self.client.login(username='admin', password='adminpass')
        response = self.client.post(
            reverse('article:delete_article', args=[self.article.id])
        )
        self.assertEqual(response.status_code, 302)  # Check for redirect after successful deletion
        self.assertFalse(Article.objects.filter(id=self.article.id).exists())
