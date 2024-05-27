from django import forms
from django.contrib.auth.forms import UserCreationForm
from reguser.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    full_name = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    image = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ('username', 'birth_date', 'full_name', 'email', 'image', 'password1', 'password2')
