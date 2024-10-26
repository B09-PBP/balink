from django.urls import path
from article.views import show_article_page, MakeArticleForm, delete_article, inside_article

app_name = 'article'

urlpatterns = [
    path('',show_article_page , name='show_article_page'),
    path('create/', MakeArticleForm, name='make_article_form'),
    path('delete/<int:id>/', delete_article, name='delete_article'),
    path('article/<int:id>/', inside_article, name='inside_article'),
]