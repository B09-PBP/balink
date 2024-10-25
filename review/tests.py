from django.forms import ValidationError
from django.test import TestCase, Client
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