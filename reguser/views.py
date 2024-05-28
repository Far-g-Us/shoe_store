from django.views.generic import FormView, CreateView, ListView, RedirectView
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth import login, logout, authenticate
from .models import CustomUser
# from datetime import datetime
# from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect



class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'login.html'
    success_url = '/'
    # success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        error_message = 'Неверный логин или пароль'
        return render(self.request, self.template_name, {'form': form, 'error': error_message})


class RegisterView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.username = form.cleaned_data['username']
        user.set_password(form.cleaned_data['password1'])
        user.save()
        userprofile = CustomUser.objects.get(username=user.username)
        userprofile.full_name = form.cleaned_data['full_name']
        userprofile.birthday = form.cleaned_data['birthday']
        userprofile.image = form.cleaned_data['image']
        userprofile.email = form.cleaned_data['email']
        userprofile.user = user
        userprofile.save()
        print(userprofile)
        login(self.request, user)
        return redirect('login')

    def form_invalid(self, form):
        print(form.errors)
        return render(self.request, self.template_name, {'formuser': form, 'error': 'Пароли должны совпадать'})


class LogoutView(RedirectView):
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)



# class UserProfileView(LoginRequiredMixin, ListView):


# def profileView(request):
#     user_profile = request.user.userprofile
#     return render(request, './profile/profile.html', {'user_profile': user_profile})
#
# def profileupView(request):
#     user_profile = request.user.userprofile
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST, instance=user_profile)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Профиль успешно обновлён')
#             return redirect('profile')
#     else:
#         form = CustomUserCreationForm(instance=user_profile)
#         return render(request, 'profile/profileup.html', {'form': form})