from django.db import models
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from mptt.models import MPTTModel, TreeForeignKey
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.conf import settings
from reguser.models import CustomUser


class Gender(models.Model):
    name = models.CharField(max_length=25, db_index=True, verbose_name='Пол')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Пол'
        verbose_name_plural = 'Пол'

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

class CountryOfManufacture(models.Model):
    name = models.CharField(max_length=50, db_index=True, verbose_name='Страна производитель')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Страна производитель'
        verbose_name_plural = 'Страны производители'

class BrandOfManufacture(models.Model):
    name = models.CharField(max_length=25, db_index=True, verbose_name='Бренд производителя')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Бренд производитель'
        verbose_name_plural = 'Бренды производители'

class CollectionProduct(models.Model):
    name = models.CharField(max_length=40, db_index=True, verbose_name='Коллекция')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Коллекция'
        verbose_name_plural = 'Коллекции'


class UpperMaterialProduct(models.Model):
    name = models.CharField(max_length=65, db_index=True, verbose_name='Материал верха')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Материал верха'
        verbose_name_plural = 'Материалы верха'

class LiningMaterialProduct(models.Model):
    name = models.CharField(max_length=65, db_index=True, verbose_name='Материал подкладки')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Материал подкладки'
        verbose_name_plural = 'Материалы подкладок'

class OutsoleMaterialProduct(models.Model):
    name = models.CharField(max_length=65, db_index=True, verbose_name='Материал подошвы')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Материал подошвы'
        verbose_name_plural = 'Материалы подошв'

class InsoleMaterialProduct(models.Model):
    name = models.CharField(max_length=65, db_index=True, verbose_name='Материал стельки')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Материал стельки'
        verbose_name_plural = 'Материалы стелек'

class Category(MPTTModel):
    name = models.CharField(max_length=160)
    url = models.SlugField(max_length=160, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_by_category', kwargs={'url': self.url})

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Shoes(models.Model):
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=40, verbose_name='Название', db_index=True)
    url = models.SlugField(max_length=130, db_index=True, unique=True)
    brand = models.ManyToManyField(BrandOfManufacture, max_length=100, verbose_name='Бренд', related_name='brand_of_manufacture_product', blank=True)
    gender = models.ManyToManyField(Gender, max_length=40, verbose_name='Пол', related_name='gender', blank=True)
    color = models.ManyToManyField(ColorProduct, max_length=40,  verbose_name='Цвет обуви', related_name='color_product')
    size = models.ManyToManyField(SizeProduct, max_length=40,  verbose_name='Размер обуви', related_name='size_product')
    upper_material = models.ManyToManyField(UpperMaterialProduct, max_length=75, verbose_name='Материал верха', related_name='upper_material_product')
    lining_material = models.ManyToManyField(LiningMaterialProduct, max_length=50, verbose_name='Материал подкладки', related_name='lining_material_product')
    outsole_material = models.ManyToManyField(OutsoleMaterialProduct, max_length=50, verbose_name='Материал подошвы', related_name='outsole_material_product')
    insole_material = models.ManyToManyField(InsoleMaterialProduct, max_length=50, verbose_name='Материал стельки', related_name='insole_material_product')
    main_image = models.ImageField(verbose_name='Основное фото', upload_to='product/%Y/%m', blank=True)
    image_1 = models.ImageField(verbose_name='Фото №1', upload_to='content/%Y/%m', blank=True, null=True)
    image_2 = models.ImageField(verbose_name='Фото №2', upload_to='content/%Y/%m', blank=True, null=True)
    image_3 = models.ImageField(verbose_name='Фото №3', upload_to='content/%Y/%m', blank=True, null=True)
    description = models.TextField(verbose_name='О товаре', blank=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        verbose_name="Цена, руб.",
        validators=[MinValueValidator(Decimal("0.01"))],
        null=False
    )
    discount = models.DecimalField(
        max_digits=5,
        decimal_places=0,
        default=0,
        verbose_name="Скидка, %",
        validators=[
            MinValueValidator(Decimal("0")),  # Скидка ≥ 0%
            MaxValueValidator(Decimal("100"))  # Скидка ≤ 100%
        ],
        null=False
    )
    stock = models.PositiveIntegerField(verbose_name='Осталось', blank=True)
    country_of_manufacture = models.ManyToManyField(CountryOfManufacture, max_length=10, verbose_name='Страна производитель', related_name='country_of_manufacture_product', blank=True)
    manufacturers_code = models.CharField(max_length=10, verbose_name='Код производителя', blank=True, help_text='"Код товара должен состоять из 5-6 цифр"')
    available = models.BooleanField(default=True)
    collection = models.ManyToManyField(CollectionProduct, max_length=40,  verbose_name='Коллекция', related_name='collection_product')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def discounted_price(self):
        """Автоматический расчёт цены со скидкой."""
        if self.price is None or self.discount is None:
            return Decimal("0.00")

        original_price = self.price
        discount_percent = self.discount

        discount_factor = Decimal("1") - (discount_percent / Decimal("100"))
        return (original_price * discount_factor).quantize(Decimal("0.00"))

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if not reviews.exists():
            return 0.0
        total = sum(review.star.value for review in reviews)
        return round(total / reviews.count(), 1)

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'url': self.url, 'id': self.id})

    class Meta:
        verbose_name = 'Обувь'
        verbose_name_plural = 'Обувь'


class RatingStar(models.Model):
    value = models.PositiveSmallIntegerField(verbose_name='Значение', default=0)

    def __str__(self):
        return str(self.value)

    class Meta:
        verbose_name = 'Звезда рейтинга'
        verbose_name_plural = 'Звёзды рейтинга'


class Review(models.Model):
    shoes = models.ForeignKey(
        Shoes,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Товар'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    text = models.TextField(verbose_name='Текст отзыва', max_length=5000, blank=True)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name='Оценка')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey(
        'self',
        verbose_name='Родитель',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.user} - {self.shoes}"

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Comment(models.Model):
    shoes = models.ForeignKey(
        Shoes,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Товар'
    )
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )
    text = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Комментарии'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Комментарий от {self.author} к {self.shoes}'

    def clean(self):
        if self.parent and self.parent.parent:
            raise ValidationError("Максимальная вложенность - 1 уровень")
        super().clean()

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={
            'url': self.shoes.url,
            'id': self.shoes.id
        }) + f'#comment-{self.id}'
