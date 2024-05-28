from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, RedirectView, FormView, TemplateView, UpdateView
from reguser.forms import CustomUserCreationForm, LoginForm
from reguser.models import CustomUser
from django.urls import reverse_lazy
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.db import transaction
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image


def resize_image(image):
    img = Image.open(image)
    img = img.resize((300, 300), Image.Resampling.LANCZOS)

    image_io = BytesIO()
    img.save(image_io, format='JPEG')
    image_data = image_io.getvalue()

    return ContentFile(image_data)


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, 'Неверный логин или пароль')
            return super().form_invalid(form)


class RegisterView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        with transaction.atomic():
            user = form.save(commit=False)
            user.username = form.cleaned_data['username']
            user.set_password(form.cleaned_data['password1'])
            user.save()

            customUser = CustomUser.objects.get(username=user.username)
            customUser.full_name = form.cleaned_data['full_name']
            customUser.birthday = form.cleaned_data['birthday']
            customUser.image = resize_image(form.cleaned_data['image'])
            customUser.email = form.cleaned_data['email']
            customUser.user = user
            customUser.save()

            print(customUser)
            login(self.request, user)
            return redirect('login')

    def form_invalid(self, form):
        print(form.errors)
        return render(self.request, self.template_name, {'formuser': form, 'error': 'Поля должны быть заполнены.'})

def LogoutView(request):
    logout(request)
    return redirect('home')


class ProfileView(LoginRequiredMixin, TemplateView):
    model = CustomUser
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customuser'] = self.request.user
        return context


# class ProfileUpdateView(LoginRequiredMixin, UpdateView):
#     form_class = UserProfileUpdateForm
#     template_name = 'profile_update.html'
#     # success_url = reverse_lazy('profile')
#
#     def get_object(self, queryset=None):
#         return self.request.user
#
#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs['instance'] = self.request.user
#         return kwargs
#
#     def get_success_url(self):
#         return reverse_lazy('profile')
#
#
# @login_required
# def update_profile(request):
#     if request.method == 'POST':
#         form = UserProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
#
#         if form.is_valid():
#             form.save()
#             return reverse_lazy('profile')  # Replace 'profile' with the appropriate URL name for the user profile page
#     else:
#         form = UserProfileUpdateForm(instance=request.user.userprofile)
#
#     context = {
#         'form': form,
#     }
#
#     return render(request, 'profile_update.html', context)