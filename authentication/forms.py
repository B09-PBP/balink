from django.contrib.auth.forms import UserCreationForm
from django import forms
from authentication.models import UserProfile
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(label = "Email", required=True)
    full_name = forms.CharField(label = "Name", required=True)

    class Meta:
        model = User
        fields = ("username", "full_name","email","password", "password_second")

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        if commit:
            user.save()
        UserProfile.objects.create(
            user = user,
            full_name = self.cleaned_data["full_name"],
            user_type = self.cleaned_data["user_type"]
        )
        return user