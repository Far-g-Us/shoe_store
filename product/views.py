from django.shortcuts import render
from django.views.generic import ListView, DetailView
from product.models import Product

class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'

