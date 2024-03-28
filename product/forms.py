from django import forms
from product.models import Product, OuterwearClothingProduct, JeansClothingProduct, CareInstructionsModel, Tshirts_and_longsleevesClothingProduct, Hoodies_and_sweatshirtsClothingProduct, TrousersClothingProduct, ShirtsClothingProduct, SportClothingProduct, ShortsClothingProduct

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product, CareInstructionsModel
        fields = ['name', 'image', 'description', 'price', 'volume', 'care_instructions', 'clothing_category']


class OuterwearForm(forms.ModelForm):
    class Meta:
        model = OuterwearClothingProduct, CareInstructionsModel
        fields = ['name', 'image', 'description', 'price', 'volume',  'care_instructions', 'clothing_category']


class JeansForm(forms.ModelForm):
    class Meta:
        model = JeansClothingProduct, CareInstructionsModel
        fields = ['name', 'image', 'description', 'price', 'volume', 'care_instructions', 'clothing_category']
                  #'lining_material', 'fashion', 'style', 'compound',


class Tshirts_and_longsleevesForm(forms.ModelForm):
    class Meta:
        model = Tshirts_and_longsleevesClothingProduct, CareInstructionsModel
        fields = ['name', 'image', 'description', 'price', 'volume', 'care_instructions', 'clothing_category']


class Hoodies_and_sweatshirtsForm(forms.ModelForm):
    class Meta:
        model = Hoodies_and_sweatshirtsClothingProduct, CareInstructionsModel
        fields = ['name', 'image', 'description', 'price', 'volume', 'care_instructions', 'clothing_category']


class TrousersForm(forms.ModelForm):
    class Meta:
        model = TrousersClothingProduct, CareInstructionsModel
        fields = ['name', 'image', 'description', 'price', 'volume', 'care_instructions', 'clothing_category']


class ShirtsForm(forms.ModelForm):
    class Meta:
        model = ShirtsClothingProduct, CareInstructionsModel
        fields = ['name', 'image', 'description', 'price', 'volume', 'care_instructions', 'clothing_category']


class SportForm(forms.ModelForm):
    class Meta:
        model = SportClothingProduct, CareInstructionsModel
        fields = ['name', 'image', 'description', 'price', 'volume', 'care_instructions', 'clothing_category']


class ShortsForm(forms.ModelForm):
    class Meta:
        model = ShortsClothingProduct, CareInstructionsModel
        fields = ['name', 'image', 'description', 'price', 'volume', 'care_instructions', 'clothing_category']