from django import forms
from product.models import Shoes, Review


class ShoesForm(forms.ModelForm):
    class Meta:
        model = Shoes
        fields = ['name', 'gender', 'color', 'size', 'main_image', 'description', 'price', 'stock', 'collection', 'country_of_manufacture', 'manufacturers_code']

class FilterForm(forms.Form):
    price__gte = forms.DecimalField(required=False,widget=forms.NumberInput(attrs={'class': 'form-control'}))
    price__lte = forms.DecimalField(required=False,widget=forms.NumberInput(attrs={'class': 'form-control'}))

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name', 'image', 'email', 'text']