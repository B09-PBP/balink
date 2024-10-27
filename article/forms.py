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
                'placeholder': 'Masukkan judul artikel'
            }),
            'content': forms.Textarea(attrs={
                'class': 'block w-full p-2 border rounded resize-none h-32 overflow-y-auto',
                'placeholder': 'Masukkan konten artikel'
            }),
            'image': forms.URLInput(attrs={
                'class': 'block w-full p-2 border rounded',
                'placeholder': 'Masukkan URL gambar utama'
            }),
            'image1': forms.URLInput(attrs={
                'class': 'block w-full p-2 border rounded',
                'placeholder': 'Masukkan URL gambar tambahan 1'
            }),
            'image2': forms.URLInput(attrs={
                'class': 'block w-full p-2 border rounded',
                'placeholder': 'Masukkan URL gambar tambahan 2'
            }),
            'image3': forms.URLInput(attrs={
                'class': 'block w-full p-2 border rounded',
                'placeholder': 'Masukkan URL gambar tambahan 3'
            }),
        }
