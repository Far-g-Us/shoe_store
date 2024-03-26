from django.db import models

class Face(models.Model):
    title = models.CharField(max_length=35, verbose_name='Название')
    image = models.ImageField(verbose_name='Фото', upload_to='content/%Y/%m', blank=True)

    def __str__(self):
        return f'{self.title}'
