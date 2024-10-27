from django.db import models
from django.contrib.auth.models import User
from product.models import Product

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    note = models.TextField(default="There's no note yet")

    # High = H, Medium = M, Low = L
    priority = models.CharField(max_length=1, default='M')

    # Reminder date for when the user wants to revisit the bookmark
    reminder = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.product.name} by {self.user.username}'