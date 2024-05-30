from django.db import models
from product.models import Shoes
from reguser.models import CustomUser


class Face(models.Model):
    pass


class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    shoes = models.ForeignKey(Shoes, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class Contact(models.Model):
    pass
