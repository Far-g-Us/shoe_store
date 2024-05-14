import django_filters
from .models import Shoes, Gender, ColorProduct, SizeProduct, CountryOfManufacture, CollectionProduct

class ShoesFilter(django_filters.FilterSet):
    brand = django_filters.CharFilter(label='Бренд')
    gender = django_filters.ModelMultipleChoiceFilter(label='Пол', queryset=Gender.objects.all())
    color = django_filters.ModelMultipleChoiceFilter(label='Цвет', queryset=ColorProduct.objects.all())
    size = django_filters.ModelMultipleChoiceFilter(label='Размер', queryset=SizeProduct.objects.all())
    country_of_manufacture = django_filters.ModelMultipleChoiceFilter(label='Страна производства', queryset=CountryOfManufacture.objects.all())
    collection = django_filters.ModelMultipleChoiceFilter(label='Коллекция', queryset=CollectionProduct.objects.all())
    discount = django_filters.NumberFilter(label='Скидка')
    price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price__lte = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Shoes
        fields = ['brand', 'gender', 'color', 'size', 'country_of_manufacture', 'collection', 'discount', 'price']

    def filter_queryset(self, queryset, name, value):
        if name in ['gender', 'color', 'size', 'country_of_manufacture', 'collection']:
            return queryset.filter(**{f'{name}__id__in': value})
        elif name == 'brand':
            return queryset.filter(brand__icontains=value)
        elif name == 'discount':
            return queryset.filter(discount=value)
        return super().filter_queryset(queryset, name, value)