from django.shortcuts import render
from django.views.generic import ListView, DetailView
from product.models import Boots

class ProductListView(ListView):
    model = Boots
    template_name = 'product_list.html'

class ProductDetailView(DetailView):
    model = Boots
    template_name = 'product_detail.html'

