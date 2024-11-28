from django import forms
from django.forms import ModelForm
from article.models import Article

class ArticleForms(ModelForm):
    class Meta:
        model = Article
        fields = ["title", "content", "image", "image1", "image2", "image3"]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'block w-full p-2 border rounded',
                'placeholder': 'Enter article title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'block w-full p-2 border rounded resize-none h-32 overflow-y-auto',
                'placeholder': 'Enter article content'
            }),
            'image': forms.URLInput(attrs={
                'class': 'block w-full p-2 border rounded',
                'placeholder': 'Enter main image URL'
            }),
            'image1': forms.URLInput(attrs={
                'class': 'block w-full p-2 border rounded',
                'placeholder': 'Enter additional image 1 URL'
            }),
            'image2': forms.URLInput(attrs={
                'class': 'block w-full p-2 border rounded',
                'placeholder': 'Enter additional image 2 URL'
            }),
            'image3': forms.URLInput(attrs={
                'class': 'block w-full p-2 border rounded',
                'placeholder': 'Enter additional image 3 URL'
            }),
        }
