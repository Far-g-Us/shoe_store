from django.db import models
from django.urls import reverse


class ColorProduct(models.Model):
    name = models.CharField(max_length=40, db_index=True, verbose_name='Цвет')

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'

    def __str__(self):
        return self.name


class SizeProduct(models.Model):
    name = models.CharField(max_length=10, db_index=True, verbose_name='Размер')

    class Meta:
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'

    def __str__(self):
        return self.name


class CollectionProduct(models.Model):
    name = models.CharField(max_length=40, db_index=True, verbose_name='Коллекция')

    class Meta:
        verbose_name = 'Коллекция'
        verbose_name_plural = 'Коллекции'

    def __str__(self):
        return self.name

class DiscountProduct(models.Model):
    name = models.CharField(max_length=40, db_index=True, verbose_name='Скидка')
    value = models.IntegerField(verbose_name='%')

    class Meta:
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    # def get_absolute_url(self):
    #     return reverse('product:product_list_by_category', args=[self.slug])

    def __str__(self):
        return self.name


class Shoes(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=40, db_index=True, verbose_name='Название')
    slug = models.SlugField(max_length=100, db_index=True)
    color = models.ManyToManyField(ColorProduct, max_length=40,  verbose_name='Цвет кросовок')
    size = models.ManyToManyField(SizeProduct, max_length=40,  verbose_name='Размер кросовок')
    image = models.ImageField(verbose_name='Фото', upload_to='content/%Y/%m', blank=True)
    description = models.TextField(verbose_name='О товаре', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Цена, руб.')
    discount = models.DecimalField(max_digits=4, decimal_places=0, default=0, verbose_name='Скидка, %', null=True)
    stock = models.PositiveIntegerField(verbose_name='Осталось', blank=True)
    available = models.BooleanField(default=True)
    collection = models.ManyToManyField(CollectionProduct, max_length=40,  verbose_name='Коллекция')

    class Meta:
        verbose_name_plural = 'Обувь'
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    # def get_absolute_url(self):
    #     return reverse('shop:product_detail_by_category', args=[self.id, self.slug])

    def __str__(self):
        return self.name

