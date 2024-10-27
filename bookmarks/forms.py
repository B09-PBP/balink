from django import forms
from bookmarks.models import Bookmark

class BookmarkForm(forms.ModelForm):
    note = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            "class": "note block p-2.5 w-full text-sm text-gray-900 rounded-lg border border-gray-300 focus:ring-primary-500 focus:border-primary-500 bg-slate-200 border-gray-600 dark:placeholder-gray-400 text-grey-900 dark:focus:ring-primary-500 dark:focus:border-primary-500",
            "rows": 5,
            "placeholder": "Add a note for this bookmark...",
        })
    )
    
    PRIORITY_CHOICES = [('H', 'High'), ('M', 'Medium'), ('L', 'Low')]
    priority = forms.ChoiceField(
        required=True,
        choices=PRIORITY_CHOICES,
        widget=forms.Select(attrs={
            "class": "priority border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 bg-slate-200 border-gray-600 dark:placeholder-gray-400 text-grey-900 dark:focus:ring-primary-500 dark:focus:border-primary-500",
        })
    )
    
    reminder = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={
            "class": "reminder border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 bg-slate-200 border-gray-600 dark:placeholder-gray-400 text-grey-900 dark:focus:ring-primary-500 dark:focus:border-primary-500",
            "type": "datetime-local",
            "placeholder": "Set a reminder (optional)"
        })
    )
    
    class Meta:
        model = Bookmark
        fields = ["note", "priority", "reminder"]
