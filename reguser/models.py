from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=150, verbose_name='ФИО', blank=True, null=True)
    email = models.EmailField(verbose_name='email', blank=True)
    image = models.ImageField(verbose_name='фото', upload_to='profile/%Y/%m', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
