from django.urls import path
from authentication.views import *
from cart.views import *
from django.urls import path, include

app_name = 'cart'

urlpatterns = [
    path("", show_cart, name="show_cart"),
    path('auth/', include('django.contrib.auth.urls')),
    path("booking/", booking_cart, name="booking"),
    path("history/", show_history, name="show_history"),
    path("add-to-cart/<uuid:product_id>/", add_to_cart, name="add_to_cart"),
    path("owned/", show_owned, name="show_owned"),
    path("remove/<int:car_id>", remove_car_from_cart, name="remove"),
    path("get-history/", get_history_json, name="get_history_json"),

    path("get-cart/", get_cart_json, name='get_cart_json'),
    path("get-cart-id/<int:id>", get_cart_json_by_user_id, name="get_cart_json_by_user_id"),
    path("remove-car/<int:id>", remove_car_from_cart_ajax, name="remove_car_from_cart_ajax"),
]