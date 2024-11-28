from django.forms import ValidationError
from django.test import TestCase, Client
from authentication.models import UserProfile
from product.models import Product
from cart.models import History
from django.contrib.auth.models import User
from django.urls import reverse

class CartTestCase(TestCase):
    def setUp(self):
        # Create a test user and login
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.login(username="testuser", password="testpassword")
        
        # Create a UserProfile with the correct field name for user privilege
        self.user_profile = UserProfile.objects.create(user=self.user, name="Test User", privilege="customer")
        
        # Add a test product to use in the tests
        self.product = Product.objects.create(
            name="Test Product",
            year=2022,
            price=100000,
            km_driven=30000,
            image_url="https://test.com/image.jpg",
            dealer="Test Dealer"
        )

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

    # Test booking an empty cart
    def test_booking_empty_cart(self):
        response = self.client.post(reverse("cart:booking_cart_ajax"), {})
        
        # Check response for empty cart
        self.assertJSONEqual(response.content, {
            'status': 'error',
            'message': 'Booking failed. Cart is empty.'
        })
        
        # Ensure no History entry was created
        self.assertEqual(History.objects.filter(user=self.user).count(), 0)

    # Test booking with invalid form data
    def test_booking_with_invalid_data(self):
        # Add product to cart but submit with missing form data
        self.user_profile.cart.add(self.product)
        response = self.client.post(reverse('cart:booking_cart_ajax'), {})
        
        # Check response for invalid form data
        self.assertJSONEqual(response.content, {
            'status': 'error',
            'message': 'Booking failed. Please check your form data.'
        })
        # Ensure no History entry was created
        self.assertEqual(History.objects.filter(user=self.user).count(), 0)

    # Test adding multiple products to cart
    def test_add_multiple_products_to_cart(self):
        product2 = Product.objects.create(
            name="Test Product 2",
            year=2023,
            price=200000,
            km_driven=15000,
            image_url="https://test.com/image2.jpg",
            dealer="Test Dealer"
        )
        
        # Add both products to cart
        self.client.get(reverse('cart:add_to_cart', args=[self.product.id]))
        self.client.get(reverse('cart:add_to_cart', args=[product2.id]))
        
        self.user_profile.refresh_from_db()
        self.assertIn(self.product, self.user_profile.cart.all())
        self.assertIn(product2, self.user_profile.cart.all())

    # Test total price calculation in the cart
    def test_cart_total_price_calculation(self):
        product2 = Product.objects.create(
            name="Test Product 2",
            year=2023,
            price=200000,
            km_driven=15000,
            image_url="https://test.com/image2.jpg",
            dealer="Test Dealer"
        )
        
        # Add both products to cart
        self.user_profile.cart.add(self.product)
        self.user_profile.cart.add(product2)

        response = self.client.get(reverse('cart:show_cart'))
        self.assertEqual(response.context['total_price'], 300000)
    
    # Test context data in cart page
    def test_cart_page_context_data(self):
        self.user_profile.cart.add(self.product)
        response = self.client.get(reverse('cart:show_cart'))
        
        self.assertEqual(response.context['total_items'], 1)
        self.assertEqual(response.context['total_price'], self.product.price)
        self.assertIn(self.product, response.context['cart'])

    # Test clearing cart after booking
    def test_cart_cleared_after_booking(self):
        self.user_profile.cart.add(self.product)
        self.client.post(reverse('cart:booking_cart_ajax'), {
            'name': 'Test Booking',
            'address': 'Test Address'
        })

        # Refresh and check if cart is empty after booking
        self.user_profile.refresh_from_db()
        self.assertEqual(self.user_profile.cart.count(), 0)

    # Test booking a large quantity of items
    def test_booking_high_quantity_cart(self):
        for i in range(10):
            Product.objects.create(
                name=f"Test Product {i}",
                year=2023,
                price=50000,
                km_driven=10000 + i * 1000,
                image_url=f"https://test.com/image{i}.jpg",
                dealer="Test Dealer"
            )

        products = Product.objects.all()
        for product in products:
            self.user_profile.cart.add(product)

        response = self.client.post(reverse('cart:booking_cart_ajax'), {
            'name': 'Bulk Booking',
            'address': 'Bulk Address'
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(History.objects.filter(user=self.user).count(), 1)
        self.assertEqual(self.user_profile.cart.count(), 0)  # Cart should be cleared

     # Test if booking updates user's profile history
    def test_booking_updates_user_history(self):
        self.user_profile.cart.add(self.product)
        self.client.post(reverse('cart:booking_cart_ajax'), {
            'name': 'Test Booking',
            'address': 'Test Address'
        })

        # Check that history was updated
        history_count = History.objects.filter(user=self.user).count()
        self.assertEqual(history_count, 1)

    # Test cart summary display
    def test_cart_summary_display(self):
        self.user_profile.cart.add(self.product)
        response = self.client.get(reverse('cart:show_cart'))
        
        # Check that the cart summary includes the product name and price
        self.assertContains(response, "Test Product")
        self.assertContains(response, "100000")  # Price as a string in the template
