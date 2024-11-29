from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import AppUser

class AppUserSignUpForm(UserCreationForm):
    class Meta:
        model = AppUser
        fields = ['user_name', 'email', 'date_of_birth', 'password']