from django import forms
from django.contrib.auth.forms import UserCreationForm
from reguser.models import CustomUser
from datetime import date


class CustomUserCreationForm(UserCreationForm):
    def clean_birthday(self):
        birthday = self.cleaned_data.get('birthday')
        if birthday and birthday > date.today():
            raise forms.ValidationError('Invalid birthday')
        return birthday

    class Meta:
        model = CustomUser
        fields = ['username', 'birthday', 'full_name', 'email', 'image', 'password1', 'password2']
