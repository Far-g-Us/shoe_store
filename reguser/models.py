from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError('Users must have a username')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        user = self.create_user(username, email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    username = models.CharField(max_length=35, unique=True)
    full_name = models.CharField(max_length=150, verbose_name='ФИО', blank=True, null=True)
    birthday = models.DateField(verbose_name='Дата рождения', blank=True, null=True)
    email = models.EmailField(verbose_name='email', blank=True)
    image = models.ImageField(verbose_name='фото', upload_to='profile/%Y/%m', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    class Meta:
        verbose_name_plural = 'Профили пользователей'

    def __str__(self):
        return f"{self.username} - {self.email} - {self.created_at}"


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        CustomUser.objects.create(username=instance.username, email=instance.email, full_name=instance.full_name, birthday=instance.birthday, image=instance.image)



def save_user_profile(sender, instance, **kwargs):
    instance.customuser.save()