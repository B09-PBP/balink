from django.urls import path
from review.views import ride_to_review, create_review, form_review
from review.views import show_main, show_json, show_json_by_id

app_name = 'review'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('ride-to-review', ride_to_review, name='ride_to_review'),
    path('create-review', create_review, name='create_review'),
    path('json/', show_json, name='show_json'),
    path('json/<int:id>/', show_json_by_id, name='show_json_by_id'),
    path('form-review/<uuid:uuid>/', form_review, name='form_review'),
]