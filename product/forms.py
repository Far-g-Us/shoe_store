from django import forms
from django.core.exceptions import ValidationError
from product.models import Shoes, Review, RatingStar, Comment
# from django.conf import settings


class ShoesForm(forms.ModelForm):
    class Meta:
        model = Shoes
        fields = ['name', 'brand', 'gender', 'color', 'size', 'main_image', 'description', 'price', 'stock', 'collection', 'country_of_manufacture', 'manufacturers_code']

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price is None:
            raise forms.ValidationError("Цена не может быть пустой.")
        return price


class FilterForm(forms.Form):
    price__gte = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    price__lte = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'star']
        exclude = ['user', 'shoes']

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


class CommentForm(forms.ModelForm):
    parent_id = forms.IntegerField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = Comment
        fields = ['text', 'parent_id']

    def clean_parent_id(self):
        parent_id = self.cleaned_data.get('parent_id')
        if parent_id:
            parent = Comment.objects.get(id=parent_id)
            if parent.parent:
                raise ValidationError("Можно отвечать только на основные комментарии")
        return parent_id