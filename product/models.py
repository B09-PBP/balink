# models.py
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    year = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    km_driven = models.IntegerField()
    image_url = models.URLField()  
    dealer = models.CharField(max_length=255)

    def __str__(self):
        return self.name
