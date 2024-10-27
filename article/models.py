from django.db import models
from django.contrib.auth.models import User
from product.models import Product
from django.utils import timezone


class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ride = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)  
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.URLField()
    comments = models.JSONField(default=list, blank=True)  
    image1 = models.URLField(null=True, blank=True)
    image2 = models.URLField(null=True, blank=True)
    image3 = models.URLField(null=True, blank=True)


    def add_comment(self, user, comment_content):
        """
        Add a comment to the JSON field.
        """
        new_comment = {
            'user': user.username,
            'content': comment_content,
            'timestamp': timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.comments.append(new_comment)
        self.save()


    def delete_comment(self, index):
        """
        Delete a comment by its index from the JSON field.
        """
        try:
            self.comments.pop(index)
            self.save()
        except IndexError:
            pass

    def __str__(self):
        return self.titl
