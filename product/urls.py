from django.urls import path, include
from product.views import show_product_page, show_product_detail, edit_product, add_product, delete_product, show_xml, show_json, show_json_by_id, show_xml_by_id, add_product_flutter, delete_product_flutter, edit_product_flutter

app_name = 'product'

urlpatterns = [
    path('', show_product_page, name='show_product_page'),
    path('detail/<uuid:id>/', show_product_detail, name='show_product_detail'),
    path('edit/<uuid:id>/', edit_product, name='edit_product'),
    path('edit_product_flutter/<uuid:id>', edit_product_flutter, name='edit_product_flutter'), 
    path('add_product/', add_product, name='add_product'),
    path('add_product_flutter/', add_product_flutter, name='add_product_flutter'),
    path('delete_product/<uuid:id>/', delete_product, name='delete_product'),
    path('delete_product_flutter/<uuid:id>/', delete_product_flutter, name='delete_product_flutter'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<uuid:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<uuid:id>/', show_json_by_id, name='show_json_by_id'),    
]