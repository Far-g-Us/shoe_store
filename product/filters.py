import django_filters
from .models import Shoes

class ShoesFilter(django_filters.FilterSet):
    class Meta:
        model = Shoes
        fields = {
            'brand': ['exact'],
            'gender': ['exact'],
            'color': ['exact'],
            'size': ['exact'],
            'country_of_manufacture': ['exact'],
            'collection': ['exact'],
            'discount': ['exact'],
            'price': ['gt', 'lt'],
        }