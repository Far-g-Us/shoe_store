from django.db import models
from product.models import Shoes
from reguser.models import CustomUser


class Face(models.Model):
    pass


class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total_price = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_total_price(self):
        total_price = sum(cart_item.get_total_price for cart_item in self.cartitem_set.all())
        return total_price


class CartItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    shoes = models.ForeignKey(Shoes, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)

    @property
    def get_total_price(self):
        if self.shoes:
            price = self.shoes.price
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
