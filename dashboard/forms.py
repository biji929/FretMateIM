from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class RegistrationForm(UserCreationForm):
    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            UserProfile.objects.create(user=user)
        return user
