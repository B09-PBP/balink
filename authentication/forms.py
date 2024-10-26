from django.contrib.auth.forms import UserCreationForm
from django import forms
from authentication.models import UserProfile
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    privilege = forms.ChoiceField(
        choices = (("admin", "Admin"), ("customer", "Customer")),
        label="Choose your user privelege",
        required=True
    )
    name = forms.CharField(label = "Full Name", required=True)

    class Meta:
        model = User
        fields = ("privilege", "username", "name")

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        if commit:
            user.save()
        UserProfile.objects.create(
            user = user,
            name = self.cleaned_data["name"],
            privilege = self.cleaned_data["privilege"]
        )
        return user

