from django import forms
from product.models import Shoes


class ShoesForm(forms.ModelForm):
    class Meta:
        model = Shoes
        fields = ['name', 'gender', 'color', 'size', 'main_image', 'description', 'price', 'stock', 'collection', 'country_of_manufacture', 'manufacturers_code']