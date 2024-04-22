from django.db import models
from django.urls import reverse


class ColorProduct(models.Model):
    name = models.CharField(max_length=40, db_index=True, verbose_name='Цвет')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'


class SizeProduct(models.Model):
    name = models.CharField(max_length=10, db_index=True, verbose_name='Размер')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'


class CollectionProduct(models.Model):
    name = models.CharField(max_length=40, db_index=True, verbose_name='Коллекция')
    url = models.SlugField(max_length=130, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Коллекция'
        verbose_name_plural = 'Коллекции'


# class DiscountProduct(models.Model):
#     name = models.CharField(max_length=40, db_index=True, verbose_name='Скидка, %')
#     value = models.IntegerField(verbose_name='%')
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name = 'Скидка'
#         verbose_name_plural = 'Скидки'


class Category(models.Model):
    name = models.CharField(max_length=100) #, db_index=True
    url = models.SlugField(max_length=160, unique=True) #, db_index=True

    def __str__(self):
        return self.name

    class Meta:
        #ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Shoes(models.Model):
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=40, verbose_name='Название') #, db_index=True
    url = models.SlugField(max_length=130) #, db_index=True
    color = models.ManyToManyField(ColorProduct, max_length=40,  verbose_name='Цвет обуви', related_name='color_product')
    size = models.ManyToManyField(SizeProduct, max_length=40,  verbose_name='Размер обуви', related_name='size_product')
    image = models.ImageField(verbose_name='Фото', upload_to='content/%Y/%m', blank=True)
    description = models.TextField(verbose_name='О товаре', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Цена, руб.', default=0)
    discount = models.DecimalField(max_digits=4, decimal_places=0, default=0, verbose_name='Скидка, %', null=True)
    stock = models.PositiveIntegerField(verbose_name='Осталось', blank=True)
    available = models.BooleanField(default=True)
    collection = models.ManyToManyField(CollectionProduct, max_length=40,  verbose_name='Коллекция', related_name='collection_product')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Обувь'
        #ordering = ('name',)
        #index_together = (('id', 'url'),)

class Confirm(models.Model):
    pass

class RatingStar(models.Model):
    value = models.PositiveSmallIntegerField(verbose_name='Значение', default=0)

    def __str__(self):
        return str(self.value)

    class Meta:
        verbose_name = 'Звезда рейтинга'
        verbose_name_plural = 'Звёзды рейтинга'

class Rating(models.Model):
    ip = models.CharField(verbose_name='IP адрес', max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name='звезда')
    shoes = models.ForeignKey(Shoes, on_delete=models.CharField, verbose_name='обувь')

    def __str__(self):
        return f"{self.star} - {self.shoes}"

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'

class Review(models.Model):
    email = models.EmailField()
    name = models.CharField(verbose_name='Имя', max_length=100)
    text = models.TextField(verbose_name='Сообщение', max_length=5000)
    parent = models.ForeignKey('self', verbose_name='Родитель', on_delete=models.SET_NULL, blank=True, null=True)
    shoes = models.ForeignKey(Shoes, verbose_name='Обувь', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.shoes}"

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
