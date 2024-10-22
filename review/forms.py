from django.forms import ModelForm
from review.models import Review

class ReviewEntryForm(ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "review_message"]