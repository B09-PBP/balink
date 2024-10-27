from django.urls import path
from article.views import show_article_page, MakeArticleForm, delete_article, inside_article, edit_article, add_comment, delete_comment

app_name = 'article'

urlpatterns = [
    path('',show_article_page , name='show_article_page'),
    path('create/', MakeArticleForm, name='make_article_form'),
    path('delete/<int:id>/', delete_article, name='delete_article'),
    path('article/<int:id>/', inside_article, name='inside_article'),
    path('edit/<int:id>/', edit_article, name='edit_article'),
    path('<int:article_id>/add_comment/', add_comment, name='add_comment'),
    path('<int:article_id>/delete_comment/<int:comment_index>/', delete_comment, name='delete_comment'),
]