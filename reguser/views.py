from django.views.generic import FormView, CreateView, ListView, RedirectView
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth import login, logout, authenticate
from .models import CustomUser
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
    success_url = '/'
    # success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])
        user.save()
        userprofile = CustomUser()
        userprofile.full_name = ''
        userprofile.birthday = 0
        userprofile.image = "image.png"
        userprofile.user = user
        userprofile.save()
        login(self.request, user)
        return redirect('home')

    def form_invalid(self, form):
        if 'password1' in form.errors and 'password2' in form.errors:
            error_message = 'Пароли должны совпадать'
        elif 'username' in form.errors:
            error_message = 'Это имя уже используется'
        else:
            error_message = 'Форма заполнена неверно'
        return render(self.request, self.template_name, {'formuser': form, 'error': error_message})

    # def reguser(request):
    #     if request.method == 'GET':
    #         return render(request, 'reguser/reguser.html', {'formuser': UserCreationForm()})
    #     else:
    #         if request.POST['password1'] == request.POST['password2']:
    #             try:
    #                 user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
    #                 user.save()
    #                 userprofile = CustomUser()
    #                 userprofile.first_name = ''
    #                 userprofile.last_name = ''
    #                 userprofile.age = 0
    #                 userprofile.image_profile = "image.png"
    #                 userprofile.about_me = ''
    #                 userprofile.user = user
    #                 userprofile.save()
    #                 login(request, user)
    #                 return redirect('home')
    #             except IntegrityError:
    #                 return render(request, 'reguser/reguser.html',
    #                               {'formuser': UserCreationForm(), 'error': 'Это имя уже используется'})
    #         else:
    #             return render(request, 'reguser/reguser.html',
    #                           {'formuser': UserCreationForm(), 'error': 'Пароли должны совпадать'})


class LogoutView(RedirectView):
    success_url = '/'

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