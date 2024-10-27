from django.forms import ModelForm
from review.models import Review
from django.utils.html import strip_tags

class ReviewEntryForm(ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "review_message"]

    def clean_review_message(self):
        review_message = self.cleaned_data["review_message"]
        return strip_tags(review_message)