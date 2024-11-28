from django.forms import ValidationError
from django.test import TestCase, Client
from django.urls import reverse
from authentication.models import UserProfile
from product.models import Product
from review.models import Review
from django.contrib.auth.models import User

# Create your tests here.
class mainTest(TestCase):
    # Test apakah url dapat diakses
    def test_main_url_is_exist(self):
        response = Client().get('')
        self.assertEqual(response.status_code, 200)

    # Test apakah page ini benar tidak ada
    def test_nonexistent_page(self):
        response = Client().get('/amazing/')
        self.assertEqual(response.status_code, 404)

    # Set up object untuk test models review
    def setUp(self):
        self.user = User.objects.create_user(username="thisisuser", password="pass12345")
        self.user_profile = UserProfile.objects.create(user=self.user, name="Test User", privilege="customer")
        self.product = Product.objects.create(
            name="BMW 3 Series 320d",
            year=2022,
            price=1500000.00,
            km_driven=539000,
            image_url="https://imgd-ct.aeplcdn.com/640X480/cw/ucp/stockApiImg/2DIGG8Z_bz5qwfb0_1_45672105.jpeg?q=80",
            dealer="Bali Bija Car Rental"
        )

    # Test untuk non user login
    def test_ride_to_review_redirects_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse('review:ride_to_review'))
        self.assertEqual(response.status_code, 302)

    # Test create object review
    def test_create_review(self):
        review = Review.objects.create(
            user=self.user_profile.user,
            ride=self.product,
            rating=5,
            review_message="Cool car rental; worth it!"
        )
        self.assertTrue(isinstance(review, Review))

    # Test apabila rating diluar range, error
    def test_rating_validation(self):
        review = Review(
            user=self.user_profile.user,
            ride=self.product,
            rating=-1,
            review_message="Great!"
        )
        
        with self.assertRaises(ValidationError):
            review.full_clean()

    # Test apabila input review message kosong, error
    def test_blank_review_message(self):
        review = Review(
            user=self.user_profile.user,
            ride=self.product,
            rating=3,
            review_message=""
        )
        with self.assertRaises(ValidationError):
            review.full_clean()

    # Test untuk create by ajax sukses
    def test_add_review_entry_ajax_authenticated(self):
        self.client.login(username='thisisuser', password='pass12345')
        response = self.client.post(reverse('review:add_review_entry_ajax'), {
            "product_id": self.product.id,
            "rating": 5,
            "review_message": "Great!"
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Review.objects.filter(review_message="Great!").exists())

    # Test hapus review untuk non admin
    def test_delete_review_by_non_admin_user(self):
        review = Review.objects.create(
            user=self.user_profile.user,
            ride=self.product,
            rating=4,
            review_message="Review!"
        )
        response = self.client.post(reverse('review:delete_review', args=[review.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Review.objects.filter(id=review.id).exists()) 

    # Test untuk show data by json
    def test_show_json_response(self):
        Review.objects.create(
            user=self.user_profile.user,
            ride=self.product,
            rating=4,
            review_message="Good car and service!"
        )
        response = self.client.get(reverse('review:show_json'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertIn("Good car and service!", response.content.decode())

    # Test untuk show data by json id
    def test_show_json_by_id_response(self):
        review = Review.objects.create(
            user=self.user_profile.user,
            ride=self.product,
            rating=3,
            review_message="ok."
        )
        response = self.client.get(reverse('review:show_json_by_id', args=[review.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertIn("ok.", response.content.decode())