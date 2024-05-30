import django_filters
from face.models import CartItem


class CartItemFilter(django_filters.FilterSet):
    class Meta:
        model = CartItem
        fields = {
            'product__name': ['icontains'],
        }
        related_name = 'cart_items'