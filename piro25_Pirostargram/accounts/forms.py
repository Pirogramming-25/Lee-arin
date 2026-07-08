from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "name", "profile_image")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("name", "bio", "profile_image")
