from django.forms import ValidationError
from django.test import TestCase, Client
from authentication.models import UserProfile
from product.models import Product
from cart.models import History
from django.contrib.auth.models import User
from django.urls import reverse

class CartTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="pass12345")
        self.user_profile = UserProfile.objects.create(user=self.user, name="Test User", privilege="customer")
        # Create a test product
        self.product = Product.objects.create(
            name="BMW 3 Series 320d",
            year=2022,
            price=1500000.00,
            km_driven=539000,
            image_url="https://imgd-ct.aeplcdn.com/640X480/cw/ucp/stockApiImg/2DIGG8Z_bz5qwfb0_1_45672105.jpeg?q=80",
            dealer="Bali Bija Car Rental"
        )
        # Log the user in
        self.client.login(username="testuser", password="pass12345")

    # Test if the cart page is accessible
    def test_cart_url_is_accessible(self):
        response = self.client.get(reverse('cart:show_cart'))
        self.assertEqual(response.status_code, 200)

    # Test if a nonexistent cart page returns 404
    def test_nonexistent_page(self):
        response = self.client.get('/cart/amazing/')
        self.assertEqual(response.status_code, 404)

    # Test adding a product to the cart
    def test_add_to_cart(self):
        response = self.client.get(reverse('cart:add_to_cart', args=[self.product.id]))
        self.user_profile.refresh_from_db()
        self.assertIn(self.product, self.user_profile.cart.all())

    # Test removing a product from the cart
    def test_remove_from_cart(self):
        self.user_profile.cart.add(self.product)
        response = self.client.post(reverse('cart:remove', args=[self.product.id]))
        self.user_profile.refresh_from_db()
        self.assertNotIn(self.product, self.user_profile.cart.all())

    # Test booking items from the cart
    def test_booking_cart(self):
        # Add a product to the cart
        self.user_profile.cart.add(self.product)
        response = self.client.post(reverse('cart:booking_cart_ajax'), {
            'name': 'Test Booking',
            'address': 'Test Address'
        })
        self.assertEqual(response.status_code, 200)

        # Check if the product was moved to order history
        history_entry = History.objects.filter(user=self.user, car=self.product).first()
        self.assertIsNotNone(history_entry)

        # Check if the product was removed from the cart
        self.user_profile.refresh_from_db()
        self.assertNotIn(self.product, self.user_profile.cart.all())

    # Test if an empty cart handles booking gracefully (no items to book)
    def test_booking_empty_cart(self):
        response = self.client.post(reverse('cart:booking_cart_ajax'), {
            'name': 'Test Booking',
            'address': 'Test Address'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(History.objects.filter(user=self.user).count(), 0)
