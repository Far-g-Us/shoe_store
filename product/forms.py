from django import forms
from product.models import Shoes, Review, Rating
# from django.conf import settings


class ShoesForm(forms.ModelForm):
    class Meta:
        model = Shoes
        fields = ['name', 'gender', 'color', 'size', 'main_image', 'description', 'price', 'stock', 'collection', 'country_of_manufacture', 'manufacturers_code']


class FilterForm(forms.Form):
    price__gte = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    price__lte = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))


class ReviewForm(forms.ModelForm):
    rating = forms.ModelChoiceField(queryset=Rating.objects.all(), label='Рейтинг')

    class Meta:
        model = Review
        fields = ['text', 'rating']

    def __init__(self, *args, **kwargs):
        shoes = kwargs.pop('shoes', None)
        super().__init__(*args, **kwargs)
        if shoes:
            self.fields['rating'].queryset = shoes.ratings.all()