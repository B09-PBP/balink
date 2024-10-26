from django.test import TestCase
from .models import Product
from django.urls import reverse

class ProductModelTest(TestCase):
    def setUp(self):
        Product.objects.create(name="Test Product", price=99.99)

    def test_product_creation(self):
        product = Product.objects.get(name="Test Product")
        self.assertEqual(product.price, 99.99)
        self.assertEqual(str(product), "Test Product")



class ProductViewTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name="Test Product", price=99.99)

    def test_product_list_view(self):
        response = self.client.get(reverse('product:show_product_page'))  
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Product")

