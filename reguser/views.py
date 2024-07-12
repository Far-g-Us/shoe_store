from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, FormView, TemplateView, UpdateView, DeleteView
from reguser.forms import CustomUserCreationForm, LoginForm
from reguser.models import CustomUser
from django.urls import reverse_lazy
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.db import transaction

#from utils import resize_image

from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile


def resize_image(image, output_format='WEBP'):
    img = Image.open(image)

    # Преобразуем изображение в режим RGB, если оно не в этом режиме и не является GIF
    if img.mode != 'RGB' and img.format != 'GIF':
        img = img.convert('RGB')

    img = img.resize((300, 300), Image.Resampling.LANCZOS)

    image_io = BytesIO()
    img.save(image_io, format=output_format)

    image_data = image_io.getvalue()

    # Возвращаем ContentFile с оригинальным именем файла, но с новым расширением
    new_name = f"{image.name.rsplit('.', 1)[0]}.{output_format.lower()}"
    return ContentFile(image_data, name=new_name)


# class LoginView(FormView):
#     template_name = 'login.html'
#     form_class = LoginForm
#     success_url = reverse_lazy('home')
#
#     def form_valid(self, form):
#         user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
#         if user is not None:
#             login(self.request, user)
#             return super().form_valid(form)
#         else:
#             form.add_error(None, 'Неверный логин или пароль')
#             return super().form_invalid(form)

class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm

    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user is not None:
            login(self.request, user)
            return redirect('profile')  # Перенаправляем пользователя на страницу профиля после успешного входа
        else:
            form.add_error(None, 'Неверный логин или пароль')
            return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('profile')  # Если не используете метод form_valid для перенаправления


# class RegisterView(CreateView):
#     model = CustomUser
#     form_class = CustomUserCreationForm
#     template_name = 'register.html'
#     success_url = reverse_lazy('login')
#
#     def form_valid(self, form):
#         with transaction.atomic():
#             user = form.save(commit=False)
#             user.username = form.cleaned_data['username']
#             user.set_password(form.cleaned_data['password1'])
#             user.save()
#
#             customUser = CustomUser.objects.get(username=user.username)
#             customUser.full_name = form.cleaned_data['full_name']
#             customUser.birthday = form.cleaned_data['birthday']
#             customUser.image = resize_image(form.cleaned_data['image'])
#             customUser.email = form.cleaned_data['email']
#             customUser.user = user
#             customUser.save()
#
#             print(customUser)
#             login(self.request, user)
#             return redirect('login')
#
#     def form_invalid(self, form):
#         print(form.errors)
#         return render(self.request, self.template_name, {'formuser': form, 'error': 'Поля должны быть заполнены.'})

class RegisterView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        with transaction.atomic():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()

            # Обновление дополнительных полей
            user.full_name = form.cleaned_data['full_name']
            user.birthday = form.cleaned_data['birthday']
            if form.cleaned_data['image']:
                user.image = resize_image(form.cleaned_data['image'], output_format='WEBP')
                print(f"Image URL: {user.image.url}")  # Отладочное сообщение
            user.email = form.cleaned_data['email']
            user.save()

            login(self.request, user)
            return redirect('login')

    def form_invalid(self, form):
        print(form.errors)
        return render(self.request, self.template_name, {'form': form, 'error': 'Поля должны быть заполнены.'})


class DeleteUserProfile(SuccessMessageMixin, DeleteView):
    model = CustomUser
    success_message = "User has been deleted"
    template_name = 'delete_user_confirm.html'
    success_url = reverse_lazy("home")


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
# @login_required
# def update_profile(request):
#     if request.method == 'POST':
#         form = UserProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
#
#         if form.is_valid():
#             form.save()
#             return redirect('profile')  # Replace 'profile' with the appropriate URL name for the user profile page
#     else:
#         form = UserProfileUpdateForm(instance=request.user.userprofile)
#
#     context = {
#         'form': form,
#     }
#
#     return render(request, 'profile_update.html', context)

# class ProfileUpdateView(LoginRequiredMixin, UpdateView):
#     model = CustomUser
#     form_class = UserProfileUpdateForm
#     template_name = 'profile_update.html'
#
#     def get_object(self, queryset=None):
#         obj = super().get_object(queryset)
#
#         if obj != self.request.user:
#             raise PermissionDenied
#
#         return obj
#
#     def get_success_url(self):
#         return reverse_lazy('profile')

# def update_user_field(request):
#     user = CustomUser.objects.get(id=request.user.id)  # получаем объект пользователя
#
#     if request.method == 'POST':
#         form = UserProfileUpdateForm(request.POST, instance=user)  # создаем форму с переданными данными пользователя
#         if form.is_valid():
#             form.save()  # сохраняем изменения только для указанного поля
