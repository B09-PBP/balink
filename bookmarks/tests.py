from django.test import TestCase, Client
from django.urls import reverse
from product.models import Product
from bookmarks.models import Bookmark
from django.utils import timezone
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
import json

class mainTest(TestCase):
    def setUp(self):
        # Setup user and login
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.login(username="testuser", password="testpassword")

        # Create a product instance
        self.product = Product.objects.create(
            name="Test Product", 
            year=2022, 
            price=1000000, 
            km_driven=3198, 
            image_url="https://test.com/image.jpg", 
            dealer="Mr Cool"
        )
    
    def test_main_url_is_exist(self):
        response = self.client.get(reverse("bookmarks:show_main"))
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


    def test_create_bookmark_view_post(self):
        response = self.client.post(reverse("bookmarks:create_bookmark"), {
            "note": "This is a new bookmark",
            "priority": "L",
            "reminder": timezone.now(),
            "product_id": self.product.id
        })
        self.assertEqual(response.status_code, 302)  # Redirect to bookmarks page
        self.assertTrue(Bookmark.objects.filter(note="This is a new bookmark").exists())

    def test_update_bookmark_view_post(self):
        bookmark = Bookmark.objects.create(user=self.user, product=self.product, note="Initial Note", priority="H")
        response = self.client.post(reverse("bookmarks:update_bookmark", args=[bookmark.id]), {
            "note": "Updated Note",
            "priority": "M",
            "reminder": timezone.now()
        })
        bookmark.refresh_from_db() 
        self.assertEqual(response.status_code, 201)
        self.assertEqual(bookmark.note, "Updated Note")
        self.assertEqual(bookmark.priority, "M")

    def test_delete_bookmark_view(self):
        bookmark = Bookmark.objects.create(user=self.user, product=self.product, note="To be deleted")
        response = self.client.post(reverse("bookmarks:delete_bookmark", args=[bookmark.id]))
        self.assertEqual(response.status_code, 302) 
        self.assertFalse(Bookmark.objects.filter(note="To be deleted").exists())

    def test_json_bookmarks_response(self):
        Bookmark.objects.create(user=self.user, product=self.product, note="JSON Test")
        response = self.client.get(reverse("bookmarks:get_user_bookmarks"))
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data[0]["note"], "JSON Test")

    def test_default_priority_for_new_bookmark(self):
        bookmark = Bookmark.objects.create(user=self.user, product=self.product, note="Default Priority Test")
        self.assertEqual(bookmark.priority, "M")

    def test_reminder_field_accepts_null(self):
        bookmark = Bookmark.objects.create(user=self.user, product=self.product, note="No Reminder", priority="L")
        self.assertIsNone(bookmark.reminder)

    def test_view_restricted_to_logged_in_users(self):
        self.client.logout()
        response = self.client.get(reverse("bookmarks:show_main"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/auth/login/?next=/bookmarks/")

    def test_bookmark_list_json_contains_all_fields(self):
        Bookmark.objects.create(user=self.user, product=self.product, note="Complete JSON Test", priority="H", reminder=timezone.now())
        response = self.client.get(reverse("bookmarks:get_user_bookmarks"))
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        
        # Verify the fields in the response
        expected_keys = {"pk", "note", "priority", "reminder", "product"}
        self.assertTrue(all(key in data[0] for key in expected_keys))
        self.assertEqual(data[0]["note"], "Complete JSON Test")
        self.assertEqual(data[0]["priority"], "High")

    def test_bookmark_retrieval_via_json_by_id(self):
        bookmark = Bookmark.objects.create(user=self.user, product=self.product, note="Retrieve by ID", priority="H", reminder=timezone.now())
        response = self.client.get(reverse("bookmarks:show_json_by_id", args=[bookmark.id]))
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data[0]["fields"]["note"], "Retrieve by ID")
        self.assertEqual(data[0]["fields"]["priority"], "H")

    def test_bookmark_update_view_get_method_not_allowed(self):
        bookmark = Bookmark.objects.create(user=self.user, product=self.product, note="GET Not Allowed Test", priority="L")
        response = self.client.get(reverse("bookmarks:update_bookmark", args=[bookmark.id]))
        self.assertEqual(response.status_code, 400)