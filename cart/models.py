from django.db import models
from authentication.models import User
from product.models import Product

class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    address = models.CharField(max_length=255)
    car = models.ManyToManyField(Product)

    def __str__(self):
        return f"History for {self.user.username} on {self.date}"