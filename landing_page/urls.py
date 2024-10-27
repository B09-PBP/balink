from django.urls import path, include
from landing_page.views import show_main, about_us

app_name = 'landing_page'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('about_us/', about_us, name='about_us'),
]