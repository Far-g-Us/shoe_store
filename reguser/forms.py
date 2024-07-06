from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from reguser.models import CustomUser
from django.contrib.auth.password_validation import validate_password
from datetime import date


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'full_name', 'birthday', 'email', 'image', 'password1', 'password2']

    full_name = forms.CharField(required=True)
    birthday = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}))
    email = forms.EmailField(required=True)
    image = forms.ImageField(required=True)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        try:
            validate_password(password)
        except forms.ValidationError as error:
            self.add_error('password1', error)
        return password

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают.")
        try:
            validate_password(password2)
        except forms.ValidationError as error:
            self.add_error('password2', error)
        return password2

    def clean_birthday(self):
        birthday = self.cleaned_data.get('birthday')
        if birthday and birthday > date.today():
            raise forms.ValidationError('Неверный день рождения')
        return birthday

    def clean_username(self):
        username = self.cleaned_data['username']
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError('User с таким username уже существует.')
        return username



class LoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user or not user.is_active:
                raise forms.ValidationError('Неверное имя пользователя или пароль.')
        return cleaned_data


# class UserProfileUpdateForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)
#     email = forms.EmailField(widget=forms.EmailInput)
#     full_name = forms.CharField(widget=forms.TextInput)
#
#     class Meta:
#         model = CustomUser
#         fields = ('email', 'full_name', 'birthday', 'image', 'password')
