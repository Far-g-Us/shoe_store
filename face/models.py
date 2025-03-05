from django.db import models
from product.models import Shoes
from reguser.models import CustomUser


class Face(models.Model):
    pass

class Banner(models.Model):
    title = models.CharField(max_length=40, verbose_name='Название', db_index=True)
    description = models.TextField(verbose_name='О товаре', blank=True)
    image = models.ImageField(upload_to='banner/%Y/%m', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Баннер товара'
        verbose_name_plural = 'Банеры товаров'

class SpecialOffer(models.Model):
    title = models.CharField(max_length=40, verbose_name='Название', db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Цена, руб.', default=0)
    discount = models.DecimalField(max_digits=4, decimal_places=0, default=0, verbose_name='Скидка, %', null=True)
    image = models.ImageField(upload_to='special_offer/%Y/%m', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Товар спец. предложения'
        verbose_name_plural = 'Товары спец. предложений'

class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total_price = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_total_price(self):
        return sum(item.get_total_price for item in self.cartitem_set.all())


class CartItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    shoes = models.ForeignKey(Shoes, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)

    @property
    def get_total_price(self):
        if self.shoes:
            # Используем цену со скидкой из модели Shoes
            price = self.shoes.discounted_price
            quantity = self.quantity
            return quantity * price
        return 0


class Contact(models.Model):
    pass


class Confirm(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_confirmed = models.BooleanField(default=False)
