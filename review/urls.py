from django.urls import path
from review.views import ride_to_review, add_review_entry_ajax
from review.views import show_main, show_json, show_json_by_id

app_name = 'review'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('ride-to-review', ride_to_review, name='ride_to_review'),
    path('json/', show_json, name='show_json'),
    path('json/<int:id>/', show_json_by_id, name='show_json_by_id'),
    path('add-review-entry-ajax', add_review_entry_ajax, name='add_review_entry_ajax')
]