from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Article
from .forms import ArticleForms
from product.models import Product  # Import Product if needed
from authentication.models import UserProfile
from django.utils import timezone

class ArticleViewsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='password123')
        self.user_profile = UserProfile.objects.create(user=self.user, privilege='user')
        self.article = Article.objects.create(title='Test Article', content='This is a test article.', user=self.user)

    def test_show_article_page(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('article:show_article_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'article_page.html')
        self.assertContains(response, 'Test Article')

    def test_make_article_form(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('article:make_article_form'), {
            'title': 'New Article',
            'content': 'This is a new article.',
            'timestamp': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
            'image': 'https://via.placeholder.com/400x200?text=Main+Image',
            'image1': 'https://via.placeholder.com/400x200?text=Image+1',
            'image2': 'https://via.placeholder.com/400x200?text=Image+2',
            'image3': 'https://via.placeholder.com/400x200?text=Image+3',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertTrue(Article.objects.filter(title='New Article').exists())

    def test_delete_article(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('article:delete_article', args=[self.article.id]))
        self.assertEqual(response.status_code, 302)  # Redirect after deletion
        self.assertFalse(Article.objects.filter(id=self.article.id).exists())

    def test_inside_article(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('article:inside_article', args=[self.article.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inside_article.html')
        self.assertContains(response, 'This is a test article.')

    def test_add_comment(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('article:add_comment', args=[self.article.id]), {
            'comment_text': 'This is a comment.'
        })
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': True, 'user': 'testuser', 'comment': 'This is a comment.'})

    def test_delete_comment(self):
        self.client.login(username='testuser', password='password123')
        self.article.add_comment(self.user, 'This is a comment.')  # Assuming you have a method to add a comment
        response = self.client.post(reverse('article:delete_comment', args=[self.article.id, 0]))  # Assuming index 0
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': True})

    def test_edit_article(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('article:edit_article', args=[self.article.id]), {
            'title': 'Updated Article',
            'content': 'This is an updated article.',
            'timestamp': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
            'image': 'https://via.placeholder.com/400x200?text=Main+Image',
            'image1': 'https://via.placeholder.com/400x200?text=Image+1',
            'image2': 'https://via.placeholder.com/400x200?text=Image+2',
            'image3': 'https://via.placeholder.com/400x200?text=Image+3',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful edit
        self.article.refresh_from_db()
        self.assertEqual(self.article.title, 'Updated Article')
