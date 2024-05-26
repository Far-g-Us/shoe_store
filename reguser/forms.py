from django import forms
from django.contrib.auth.forms import UserCreationForm
from reguser.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['full_name', 'image', 'email']
