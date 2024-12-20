from django.urls import path
from review.views import show_main, ride_to_review, add_review_entry_ajax, delete_review
from review.views import show_json, show_json_by_id
from review.views import add_review_flutter, all_reviews_flutter, all_rides_flutter, delete_review_flutter, edit_review_flutter, user_review_flutter
app_name = 'review'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('ride-to-review', ride_to_review, name='ride_to_review'),
    path('json/', show_json, name='show_json'),
    path('json/<int:id>/', show_json_by_id, name='show_json_by_id'),
    path('add-review-entry-ajax', add_review_entry_ajax, name='add_review_entry_ajax'),
    path('delete-review/<int:review_id>/', delete_review, name='delete_review'),
    path('add-review-flutter/', add_review_flutter, name='add_review_flutter'),
    path('edit-review-flutter/', edit_review_flutter, name='edit_review_flutter'),
    path('user-review-flutter/', user_review_flutter, name='user_review_flutter'),
    path('all-reviews-flutter/', all_reviews_flutter, name='all_reviews_flutter'),
    path('all-rides-flutter/', all_rides_flutter, name='all_rides_flutter'),
    path('delete-review-flutter/<int:review_id>/', delete_review_flutter, name='delete_review_flutter'),
]