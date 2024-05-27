from datetime import date
from django import forms
from django.contrib.auth.forms import UserCreationForm
from reguser.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(required=False)
    birthday = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    email = forms.EmailField(required=False)
    image = forms.ImageField(required=False)

    def clean_birthday(self):
        birthday = self.cleaned_data.get('birthday')
        if birthday and birthday > date.today():
            raise forms.ValidationError('Invalid birthday')
        return birthday

    class Meta:
        model = CustomUser
        fields = ['username', 'birthday', 'full_name', 'email', 'image', 'password1', 'password2']
