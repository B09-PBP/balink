from django.test import TestCase, Client
from django.urls import reverse
from product.models import Product
from bookmarks.models import Bookmark
from django.utils import timezone
from django.contrib.auth.models import User

class mainTest(TestCase):
    def setUp(self):
        # Buat user uji dan login
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.login(username="testuser", password="testpassword")

        # Make dummy product 
        self.product = Product.objects.create(name="Test Product", year=2022,  price=1000000, km_driven=3198, image_url="https://test.com/image.jpg", dealer="Mr Cool")
        
    def test_main_url_is_exist(self):
        response = Client().get('')
        self.assertEqual(response.status_code, 200)
    
    def test_nonexistent_page(self):
        response = self.client.get('/nonexistent/')
        self.assertEqual(response.status_code, 404)

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("bookmarks:show_main"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/auth/login/?next=/bookmarks/")

    def test_bookmark_creation(self):
        bookmark = Bookmark.objects.create(
            user=self.user,
            product=self.product,
            note="Test",
            priority="H",
            reminder=timezone.now()
        )
        self.assertTrue(isinstance(bookmark, Bookmark))
        self.assertEqual(bookmark.note, "Test")
        self.assertEqual(bookmark.user, self.user)
    
    def test_bookmark_priority_level(self):
        bookmark = Bookmark.objects.create(
            user=self.user,
            product=self.product,
            note="Priority Test",
            priority="M",
            reminder=timezone.now()
        )
        self.assertEqual(bookmark.priority, "M")