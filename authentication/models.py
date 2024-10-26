from django.db import models
from django.contrib.auth.models import User
from product.models import Product

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    cart = models.ManyToManyField(Product, related_name='user_carts', blank=True)
    user_privelege = models.CharField(max_length=10, default="customer")