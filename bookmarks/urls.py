from django.urls import path
from bookmarks.views import *

app_name = 'bookmarks'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('create_bookmark/', create_bookmark, name='create_bookmark'),
    path('update_bookmark/', update_bookmark, name='update_bookmark'), 
    path('delete/<int:bookmark_id>/', delete_bookmark, name='delete_bookmark'), 
]