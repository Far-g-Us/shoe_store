from django.shortcuts import render
from django.views.generic import ListView, DetailView
from product.models import Products

class ProductListView(ListView):
    model = Products
    template_name = 'product_list.html'

class ProductDetailView(DetailView):
    model = Products
    template_name = 'product_detail.html'

