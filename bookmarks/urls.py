from django.urls import path
from bookmarks.views import show_main, show_json, show_json_by_id
from bookmarks.views import create_bookmark, update_bookmark, delete_bookmark

app_name = 'bookmarks'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('create-bookmark/', create_bookmark, name='create_bookmark'),
    path('update-bookmark/<int:id>/', update_bookmark, name='update_bookmark'), 
    path('delete-bookmark/<int:id>/', delete_bookmark, name='delete_bookmark'), 
    path('json/', show_json, name='show_json'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
]