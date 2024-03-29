from django.db import models


class ColorProduct(models.Model):
    name = models.CharField(max_length=40, verbose_name='Цвет')

    class Meta:
        verbose_name_plural = 'Цвет'

    def __str__(self):
        return self.name


class SizeProduct(models.Model):
    name = models.CharField(max_length=10, verbose_name='Размер')

    class Meta:
        verbose_name_plural = 'Размер'

    def __str__(self):
        return self.name


class CollectionProduct(models.Model):
    name = models.CharField(max_length=40, verbose_name='Коллекция')

    class Meta:
        verbose_name_plural = 'Коллекция'

    def __str__(self):
        return self.name


class Shoes(models.Model):
    name = models.CharField(max_length=40, verbose_name='Кросовки')
    color = models.ManyToManyField(ColorProduct, max_length=40,  verbose_name='Цвет кросовок')
    size = models.ManyToManyField(SizeProduct, max_length=40,  verbose_name='Размер кросовок')
    image = models.ImageField(verbose_name='Фото', upload_to='content/%Y/%m', blank=True)
    description = models.TextField(verbose_name='О товаре', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    volume = models.CharField(max_length=100, verbose_name='Кол-во', blank=True, null=True)
    collection = models.ManyToManyField(CollectionProduct, max_length=40,  verbose_name='Коллекция')

    class Meta:
        verbose_name_plural = 'Обувь'

    def __str__(self):
        return self.name

