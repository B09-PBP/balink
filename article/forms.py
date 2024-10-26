from django.forms import ModelForm
from article.models import Article

class ArticleForms(ModelForm):
    class Meta:
        model = Article
        fields = ["title", "content", "image"]