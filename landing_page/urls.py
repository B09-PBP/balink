from django.urls import path, include
from landing_page.views import show_main

app_name = 'landing_page'

urlpatterns = [
    path('', show_main, name='show_main'),
]