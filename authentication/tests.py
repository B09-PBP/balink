from django.test import TestCase
from django.contrib.auth.models import User
from product.models import Product
from .models import UserProfile
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import get_user_model
from authentication.forms import RegisterForm
from authentication.models import UserProfile

class UserProfileModelTest(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        # Create a UserProfile for the user
        self.user_profile = UserProfile.objects.create(user=self.user, name='Test User', privilege='admin')

    def test_user_profile_creation(self):
        """Test if a UserProfile instance is created properly"""
        self.assertIsInstance(self.user_profile, UserProfile)
        self.assertEqual(self.user_profile.name, 'Test User')
        self.assertEqual(self.user_profile.privilege, 'admin')
        self.assertEqual(self.user_profile.user.username, 'testuser')

    def test_user_profile_string_representation(self):
        """Test the string representation of the user profile"""
        self.assertEqual(str(self.user_profile), self.user_profile.name)

    def test_cart_relationship(self):
        """Test the ManyToMany relationship with Product"""
        product1 = Product.objects.create(
            name="Product A",
            year=2020,
            price=5000.00,
            km_driven=10000,
            image_url="https://example.com/imageA.jpg",
            dealer="Dealer A"
        )
        product2 = Product.objects.create(
            name="Product B",
            year=2018,
            price=7000.00,
            km_driven=15000,
            image_url="https://example.com/imageB.jpg",
            dealer="Dealer B"
        )

        # Add products to the user's cart
        self.user_profile.cart.add(product1, product2)

        # Check if the products are in the cart
        self.assertIn(product1, self.user_profile.cart.all())
        self.assertIn(product2, self.user_profile.cart.all())
        self.assertEqual(self.user_profile.cart.count(), 2)

    def test_cart_removal(self):
        """Test removing a product from the cart"""
        product = Product.objects.create(
            name="Product A",
            year=2020,
            price=5000.00,
            km_driven=10000,
            image_url="https://example.com/imageA.jpg",
            dealer="Dealer A"
        )
        self.user_profile.cart.add(product)

        # Remove product from cart
        self.user_profile.cart.remove(product)

        # Check if the product has been removed
        self.assertNotIn(product, self.user_profile.cart.all())


class AuthenticationURLsTest(TestCase):
    def test_register_url(self):
        url = reverse('authentication:register')
        self.assertEqual(url, '/auth/register/')  # Update the URL as per your app's structure

    def test_login_url(self):
        url = reverse('authentication:login')
        self.assertEqual(url, '/auth/login/')  # Update the URL as per your app's structure

    def test_logout_url(self):
        url = reverse('authentication:logout')
        self.assertEqual(url, '/auth/logout/')  # Update the URL as per your app's structure

class AuthenticationViewsTest(TestCase):
    def setUp(self):
        self.username = "testuser"
        self.password = "testpassword"
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_login_user_success(self):
        response = self.client.post(reverse('authentication:login'), {
            'username': self.username,
            'password': self.password
        })
        self.assertEqual(response.status_code, 302)  # Should redirect
        self.assertTrue(response.cookies.get('user_logged_in'))  # Check if cookie is set
        self.assertRedirects(response, reverse('landing_page:show_main'))

    def test_login_user_failure(self):
        response = self.client.post(reverse('authentication:login'), {
            'username': 'wronguser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)  # Should render login page again
        self.assertIn("Sorry, incorrect username or password. Please try again.", [m.message for m in messages.get_messages(response.wsgi_request)])

    def test_register_user_success(self):
        response = self.client.post(reverse('authentication:register'), {
            'username': 'newuser',
            'name': 'User One',
            'password1': 'ayamikan123',
            'password2': 'ayamikan123',
            'privilege': 'customer',
        })
        
        self.assertEqual(response.status_code, 302)  # Should redirect
        self.assertRedirects(response, reverse('authentication:login'))
        self.assertTrue(get_user_model().objects.filter(username='newuser').exists())

    def test_logout_user(self):
        self.client.login(username=self.username, password=self.password)  # Log the user in
        response = self.client.get(reverse('authentication:logout'))
        self.assertEqual(response.status_code, 302)  # Should redirect
        self.assertRedirects(response, reverse('landing_page:show_main'))
        self.assertEqual(response.cookies.get('user_logged_in').value, '')  # Check if cookie is empty

class RegisterFormTest(TestCase):

    def test_register_form_valid(self):
        form_data = {
            'username': 'newuser',
            'name': 'User One',
            'password1': 'ayamikan123',
            'password2': 'ayamikan123',
            'privilege': 'customer',
        }
        form = RegisterForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        # Save the user and check if it exists in the database
        user = form.save()
        self.assertEqual(user.username, 'newuser')
        self.assertTrue(UserProfile.objects.filter(user=user).exists())

    def test_register_form_invalid_username_taken(self):
        # Create an existing user
        get_user_model().objects.create_user(username='existinguser', password='password')
        
        form_data = {
            'username': 'existinguser',
            'name': 'User Two',
            'password1': 'newpassword',
            'password2': 'newpassword',
            'privilege': 'customer',
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertEqual(form.errors['username'], ["A user with that username already exists."])

    def test_register_form_missing_fields(self):
        form_data = {
            'username': '',
            'name': '',
            'password1': '',
            'password2': '',
            'privilege': 'customer',
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('name', form.errors)
        self.assertIn('password1', form.errors)
        self.assertIn('password2', form.errors)

    def test_register_form_password_mismatch(self):
        form_data = {
            'username': 'newuser',
            'name': 'User One',
            'password1': 'newpassword',
            'password2': 'differentpassword',
            'privilege': 'customer',
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
        self.assertEqual(form.errors['password2'], ["The two password fields didn’t match."]) 

    def test_register_view_redirects_after_success(self):
        response = self.client.post(reverse('authentication:register'), {
            'username': 'newuser',
            'name': 'User One',
            'password1': 'ayamikan123',
            'password2': 'ayamikan123',
            'privilege': 'customer',
        })

        self.assertEqual(response.status_code, 302)  # Check for redirect
        self.assertRedirects(response, reverse('authentication:login'))  # Check if redirected to login



