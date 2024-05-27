from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import FormView, CreateView, ListView
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from .models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin


class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'login.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)


class RegisterView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')


    def form_valid(self, form):
        user = form.save(commit=False)
        user.full_name = form.cleaned_data.get('full_name')
        user.birthday = form.cleaned_data.get('birthday')
        user.email = form.cleaned_data.get('email')
        user.image = form.cleaned_data.get('image')
        user.save()
        login(self.request, user)
        return super().form_valid(form)


class UserProfileView(LoginRequiredMixin, ListView):
    pass
