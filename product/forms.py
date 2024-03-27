from django import forms
from product.models import Product, OuterwearClothingProduct, JeansClothingProduct, CareInstructionsModel

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product, CareInstructionsModel
        fields = ['name', 'image', 'description', 'price', 'volume', 'care_instructions']


class OuterwearForm(forms.ModelForm):
    class Meta:
        model = OuterwearClothingProduct, CareInstructionsModel
        fields = ['name', 'image', 'description', 'price', 'volume',  'care_instructions']


class JeansForm(forms.ModelForm):
    class Meta:
        model = JeansClothingProduct, CareInstructionsModel
        fields = ['name', 'image', 'description', 'price', 'volume', 'lining_material', 'fashion', 'style', 'compound', 'care_instructions']