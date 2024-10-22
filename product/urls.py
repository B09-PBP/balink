from django.urls import path, include
from product.views import show_product_page, search_products

app_name = 'product'

urlpatterns = [
    path('', show_product_page, name='show_product_page'),
    path('search/', search_products, name='search_products'),
]