from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import AppUser


class AppUserSignUpForm(UserCreationForm):
    class Meta:
        model = AppUser
        fields = ['username', 'password1', 'password2', 'email', 'date_of_birth']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),  
        }
    