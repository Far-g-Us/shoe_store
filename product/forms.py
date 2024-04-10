from django import forms
from product.models import Shoes


class ShoesForm(forms.ModelForm):
    class Meta:
        model = Shoes
        fields = ['name', 'color', 'size', 'image', 'description', 'price', 'stock', 'collection']