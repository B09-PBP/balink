from django import forms
from product.models import Product
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags
import re

class ProductEntryForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "year", "price", "km_driven", "image_url", "dealer"]

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if not name:
            raise ValidationError("Name is required.")
        return strip_tags(name)

    def clean_dealer(self):
        dealer = self.cleaned_data.get("dealer")
        if not dealer:
            raise ValidationError("Dealer is required.")
        return strip_tags(dealer)

    def clean_image_url(self):
        image_url = self.cleaned_data.get("image_url")
        if image_url and not self.is_valid_url(image_url):
            raise ValidationError("Invalid image URL.")
        return strip_tags(image_url)

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price is None or price < 0:
            raise ValidationError("Price must be a positive number.")
        return price

    def clean_year(self):
        year = self.cleaned_data.get("year")
        if year is None or year < 1886 or year > 2100:  # Assuming cars weren't made before 1886
            raise ValidationError("Year must be between 1886 and 2100.")
        return year

    def clean_km_driven(self):
        km_driven = self.cleaned_data.get("km_driven")
        if km_driven is None or km_driven < 0:
            raise ValidationError("Kilometers driven must be a non-negative number.")
        return km_driven

    def is_valid_url(self, url):
        # Basic URL validation using regex
        regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
            r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return re.match(regex, url) is not None
