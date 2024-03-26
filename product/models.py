from django.db import models

class Products(models.Model):
    title = models.CharField(max_length=35, verbose_name='Название')
    image = models.ImageField(verbose_name='Фото', upload_to='content/%Y/%m', blank=True)
    volume = models.CharField(max_length=100, verbose_name='Кол-во', blank=True, null=True)

    description = models.TextField(verbose_name='О товаре', blank=True)

    def __str__(self):
        return f'{self.title}, {self.volume}'