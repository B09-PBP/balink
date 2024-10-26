from django.urls import path
from authentication.views import *
from cart.views import *
from django.urls import path, include

app_name = 'cart'

urlpatterns = [
    path("", show_cart, name="show_cart"),
    path('auth/', include('django.contrib.auth.urls')),
    path("history/", show_history, name="show_history"),
    path("add-to-cart/<uuid:product_id>/", add_to_cart, name="add_to_cart"),
    path("remove/<uuid:car_id>", remove_car_from_cart, name="remove"),
    path("remove-car/<uuid:id>", remove_car_from_cart_ajax, name="remove_car_from_cart_ajax"),
    path('booking-cart-ajax/', booking_cart_ajax, name='booking_cart_ajax'),
    path('json/', show_json, name='show_json'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
]