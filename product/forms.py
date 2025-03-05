from django import forms
from product.models import Shoes, Review, RatingStar
# from django.conf import settings


class ShoesForm(forms.ModelForm):
    class Meta:
        model = Shoes
        fields = ['name', 'brand', 'gender', 'color', 'size', 'main_image', 'description', 'price', 'stock', 'collection', 'country_of_manufacture', 'manufacturers_code']


class FilterForm(forms.Form):
    price__gte = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    price__lte = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'star']
        widgets = {
            'star': forms.HiddenInput()
        }


    def __init__(self, *args, **kwargs):
        kwargs.pop('shoes', None)
        # Удаляем ненужную логику с shoes, так как звезды не зависят от товара
        super().__init__(*args, **kwargs)
        # Если нужно ограничить выбор звезд (например, только 1-5)
        self.fields['star'].queryset = RatingStar.objects.filter(value__in=[1, 2, 3, 4, 5])
        self.fields['star'].label = "Оценка"