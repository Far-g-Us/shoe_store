from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, FormView, TemplateView, UpdateView, DeleteView
from reguser.forms import CustomUserCreationForm, LoginForm
from .forms import UserProfileUpdateForm, CustomPasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from reguser.models import CustomUser
from django.urls import reverse_lazy
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.db import transaction
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
#from utils import resize_image


def resize_image(image, output_format='WEBP'):
    if not image:
        return None

    try:
        # Проверка на анимированные GIF (вне зависимости от расширения)
        if image.name.lower().endswith('.gif'):
            img = Image.open(image)
            if getattr(img, 'is_animated', False):
                return ContentFile(image.read(), name=image.name)

        # Открываем изображение
        img = Image.open(image)
        original_format = img.format.upper() if img.format else ''

        # Определяем режим цвета
        if original_format == 'PNG' and img.mode == 'RGBA':
            convert_mode = 'RGBA'
        else:
            convert_mode = 'RGB'

        # Конвертация цветового пространства
        img = img.convert(convert_mode)

        # Ресайз
        img = img.resize((300, 300), Image.Resampling.LANCZOS)

        # Настройки сохранения для разных форматов
        save_args = {'format': output_format}
        if output_format == 'WEBP':
            save_args.update({'quality': 90, 'method': 6})
        elif output_format == 'JPEG':
            save_args['quality'] = 85
            save_args['subsampling'] = '4:4:4'  # Максимальное качество цветности

        # Сохраняем в буфер
        buffer = BytesIO()
        img.save(buffer, **save_args)

        # Формируем имя файла
        base_name = image.name.rsplit('.', 1)[0]
        new_name = f"{base_name}.{output_format.lower()}"

        return ContentFile(buffer.getvalue(), name=new_name)

    except Exception as e:
        print(f"Image processing error: {e}")
        # Возвращаем оригинал с сохранением имени
        return ContentFile(image.read(), name=image.name)


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
    success_message = "Пользователь удалён!"
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


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserProfileUpdateForm
    template_name = 'profile_update.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        # Обработка изображения
        if 'image' in form.files:
            image_file = form.files['image']
            processed_file = resize_image(image_file)

            # Сохраняем только если обработка прошла успешно
            if processed_file:
                form.instance.image.save(
                    processed_file.name,  # Используем имя из ContentFile
                    processed_file,
                    save=False
                )
        return super().form_valid(form)


class ChangePasswordView(LoginRequiredMixin, FormView):
    form_class = CustomPasswordChangeForm
    template_name = 'change_password.html'
    success_url = reverse_lazy('profile')

    def get_form_kwargs(self):
        """Передаем текущего пользователя в форму"""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        """Обработка валидной формы"""
        user = form.save()
        update_session_auth_hash(self.request, user)  # Сохраняем сессию
        messages.success(self.request, 'Пароль успешно изменен!')
        return super().form_valid(form)

    def form_invalid(self, form):
        """Обработка невалидной формы"""
        messages.error(self.request, 'Исправьте ошибки в форме')
        return super().form_invalid(form)