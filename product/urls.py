from django.urls import path, include
from product.views import show_product_page, show_product_detail, search_products, show_xml, show_json, show_json_by_id, show_xml_by_id

app_name = 'product'

urlpatterns = [
    path('', show_product_page, name='show_product_page'),
    path('detail/<uuid:id>', show_product_detail, name='show_product_detail'),
    path('search/', search_products, name='search_products'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<uuid:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<uuid:id>/', show_json_by_id, name='show_json_by_id'),    
]