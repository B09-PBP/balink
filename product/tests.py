from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product
import uuid
from product.forms import ProductEntryForm
from authentication.models import UserProfile

class ProductModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Toyota Corolla",
            year=2020,
            price=15000.00,
            km_driven=30000,
            image_url="https://example.com/image.jpg",
            dealer="Best Dealer"
        )

    def test_product_creation(self):
        """Test if a product instance is created properly"""
        self.assertIsInstance(self.product, Product)
        self.assertIsNotNone(self.product.id)  # Ensure UUID is generated
        self.assertEqual(self.product.name, "Toyota Corolla")
        self.assertEqual(self.product.year, 2020)
        self.assertEqual(self.product.price, 15000.00)
        self.assertEqual(self.product.km_driven, 30000)
        self.assertEqual(self.product.image_url, "https://example.com/image.jpg")
        self.assertEqual(self.product.dealer, "Best Dealer")

    def test_string_representation(self):
        """Test the string representation of the product"""
        self.assertEqual(str(self.product), self.product.name)

    def test_uuid_is_valid(self):
        """Test if the UUID field is valid"""
        try:
            uuid_obj = uuid.UUID(str(self.product.id), version=4)
        except ValueError:
            self.fail("Product ID is not a valid UUIDv4")
        self.assertEqual(str(uuid_obj), str(self.product.id))

class ProductViewTests(TestCase):
    def setUp(self):
        # Create a test user and log in
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.admin_user_profile = UserProfile.objects.create(user=self.user, privilege="admin")
        self.client.login(username='testuser', password='12345')

        # Create test products
        self.product1 = Product.objects.create(
            id=uuid.uuid4(),
            name="Product A",
            year=2020,
            price=5000.00,
            km_driven=10000,
            image_url="https://example.com/imageA.jpg",
            dealer="Dealer A"
        )
        self.product2 = Product.objects.create(
            id=uuid.uuid4(),
            name="Product B",
            year=2018,
            price=7000.00,
            km_driven=15000,
            image_url="https://example.com/imageB.jpg",
            dealer="Dealer A"
        )

    def test_show_product_page(self):
        # Test the product page view
        User.objects.filter(username='testuser').delete()
        
        current_user = User.objects.create_user(username='testuser', password='12345')
        UserProfile.objects.create(user=current_user)
        
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('product:show_product_page'), {'search': 'Product A'})
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product_page.html')
        self.assertIn('Product A', response.content.decode())

    def test_show_product_detail(self):
        # Test the product detail view
        response = self.client.get(reverse('product:show_product_detail', args=[self.product1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product_detail.html')
        self.assertIn(self.product1.name, response.content.decode())

    def test_add_product(self):
        # Test adding a new product
        response = self.client.post(reverse('product:add_product'), {
            'name': 'New Product',
            'year': 2021,
            'price': '12000.00',
            'km_driven': '5000',
            'image_url': 'https://example.com/image_new.jpg',
            'dealer': 'Dealer B'
        })
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Product.objects.filter(name="New Product").exists())

    def test_edit_product(self):
        # Test editing an existing product
        response = self.client.post(reverse('product:edit_product', args=[self.product1.id]), {
            'name': 'Updated Product A',
            'year': self.product1.year,
            'price': self.product1.price,
            'km_driven': self.product1.km_driven,
            'image_url': self.product1.image_url,
            'dealer': self.product1.dealer
        })
        self.assertEqual(response.status_code, 302)  # Redirect after save
        self.product1.refresh_from_db()
        self.assertEqual(self.product1.name, 'Updated Product A')

    def test_delete_product(self):
        # Test deleting a product
        response = self.client.post(reverse('product:delete_product', args=[self.product1.id]))
        self.assertEqual(response.status_code, 302)  # Redirect after deletion
        self.assertFalse(Product.objects.filter(id=self.product1.id).exists())

    def test_show_xml(self):
        # Test XML response for all products
        response = self.client.get(reverse('product:show_xml'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')

    def test_show_json(self):
        # Test JSON response for all products
        response = self.client.get(reverse('product:show_json'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_show_xml_by_id(self):
        # Test XML response for a single product
        response = self.client.get(reverse('product:show_xml_by_id', args=[self.product1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')
        self.assertIn(self.product1.name, response.content.decode())

    def test_show_json_by_id(self):
        # Test JSON response for a single product
        response = self.client.get(reverse('product:show_json_by_id', args=[self.product1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertIn(self.product1.name, response.content.decode())

class ProductEntryFormTest(TestCase):
    
    def setUp(self):
        # Set up valid data for the form to use as a base
        self.valid_data = {
            'name': "Sample Product",
            'year': 2020,
            'price': 15000,
            'km_driven': 50000,
            'image_url': "http://example.com/image.jpg",
            'dealer': "Sample Dealer",
        }

    def test_form_valid_data(self):
        # Test form with valid data
        form = ProductEntryForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_name_required(self):
        # Test form when name is missing
        data = self.valid_data.copy()
        data['name'] = ""
        form = ProductEntryForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("This field is required.", form.errors['name'])

    def test_dealer_required(self):
        # Test form when dealer is missing
        data = self.valid_data.copy()
        data['dealer'] = ""
        form = ProductEntryForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("This field is required.", form.errors['dealer'])

    def test_image_url_invalid(self):
        # Test form with an invalid image URL
        data = self.valid_data.copy()
        data['image_url'] = "invalid-url"
        form = ProductEntryForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("Enter a valid URL.", form.errors['image_url'])

    def test_price_positive(self):
        # Test form with a negative price
        data = self.valid_data.copy()
        data['price'] = -100
        form = ProductEntryForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("Price must be a positive number.", form.errors['price'])

    def test_km_driven_non_negative(self):
        # Test form with a negative km driven value
        data = self.valid_data.copy()
        data['km_driven'] = -500
        form = ProductEntryForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("Kilometers driven must be a non-negative number.", form.errors['km_driven'])

class ProductURLTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create an admin user and a customer user with their profiles
        cls.admin_user = User.objects.create_user(username='admin', password='adminpassword')
        cls.admin_user_profile = UserProfile.objects.create(user=cls.admin_user, privilege="admin")

        cls.customer_user = User.objects.create_user(username='customer', password='customerpassword')
        cls.customer_user_profile = UserProfile.objects.create(user=cls.customer_user, privilege="customer")

        # Create a sample product
        cls.product = Product.objects.create(
            id=uuid.uuid4(),
            name="Product A",
            year=2020,
            price=5000.00,
            km_driven=10000,
            image_url="https://example.com/imageA.jpg",
            dealer="Dealer A"
        )

    def test_show_product_page_url(self):
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(reverse('product:show_product_page'))
        self.assertEqual(response.status_code, 200)

    def test_show_product_detail_url_as_customer(self):
        self.client.login(username='customer', password='customerpassword')
        response = self.client.get(reverse('product:show_product_detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
    
    def test_show_product_detail_url_as_admin(self):
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(reverse('product:show_product_detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)

    def test_edit_product_url_as_admin(self):
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(reverse('product:edit_product', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)

    def test_add_product_url_as_admin(self):
        self.client.login(username='admin', password='adminpassword')
        
        # Test GET request to ensure the form renders correctly
        response = self.client.get(reverse('product:add_product'))
        self.assertEqual(response.status_code, 405)  # Expecting 200 for GET

        # Test POST request to ensure product can be added
        response = self.client.post(reverse('product:add_product'), {
            'name': 'Product B',
            'image_url': 'https://example.com/imageB.jpg',
            'price': 6000.00,
            'year': 2021,
            'km_driven': 5000,
            'dealer': 'Dealer B'
        })
        self.assertEqual(response.status_code, 201)  # Expecting 201 for successful creation

    def test_delete_product_url_as_admin(self):
        self.client.login(username='admin', password='adminpassword')
        response = self.client.post(reverse('product:delete_product', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)

    def test_edit_product_url_as_customer(self):
        self.client.login(username='customer', password='customerpassword')
        response = self.client.get(reverse('product:edit_product', args=[self.product.id]))
        self.assertEqual(response.status_code, 403)  # Expecting forbidden

    def test_delete_product_url_as_customer(self):
        self.client.login(username='customer', password='customerpassword')
        response = self.client.post(reverse('product:delete_product', args=[self.product.id]))
        self.assertEqual(response.status_code, 403)  # Expecting forbidden

    def test_show_xml_url(self):
        self.client.login(username='admin', password='adminpassword')  # Login required for XML
        response = self.client.get(reverse('product:show_xml'))
        self.assertEqual(response.status_code, 200)

    def test_show_json_url(self):
        self.client.login(username='admin', password='adminpassword')  # Login required for JSON
        response = self.client.get(reverse('product:show_json'))
        self.assertEqual(response.status_code, 200)

    def test_show_json_by_id_url(self):
        self.client.login(username='admin', password='adminpassword')  # Login required for specific JSON
        response = self.client.get(reverse('product:show_json_by_id', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)

    def test_show_xml_by_id_url(self):
        self.client.login(username='admin', password='adminpassword')  # Login required for specific XML
        response = self.client.get(reverse('product:show_xml_by_id', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)