from django.urls import path, include
from product.views import show_product_page

app_name = 'product'

urlpatterns = [
    path('', show_product_page, name='show_product_page'),
]