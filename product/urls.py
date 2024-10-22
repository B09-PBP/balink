from django.urls import path, include
from product.views import show_product_page, search_products, show_xml, show_json, show_json_by_id, show_xml_by_id

app_name = 'product'

urlpatterns = [
    path('', show_product_page, name='show_product_page'),
    path('search/', search_products, name='search_products'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),    
]