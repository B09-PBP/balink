from django.forms import ModelForm
from product.models import Product
from django.utils.html import strip_tags

class ProductEntryForm(ModelForm):
    class Meta:
        model = Product
        fields = ["name", "year", "price", "km_driven","image_url", "dealer"]
    
    def clean_name(self):
        name = self.cleaned_data["name"]
        return strip_tags(name)

    def clean_dealer(self):
        dealer = self.cleaned_data["dealer"]
        return strip_tags(dealer)
    
    def clean_image_url(self):
        image_url = self.cleaned_data["image_url"]
        return strip_tags(image_url)