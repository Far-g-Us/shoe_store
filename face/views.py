from django.shortcuts import render
from django.views.generic import ListView, DetailView
from face.models import Face
from product.models import Shoes

class indexView(ListView):
    model = Face
    fields = '__all__'
    template_name = 'index.html'

    def get_queryset(self):
        return Face.objects.all()

class ProductDetailView(DetailView):
    model = Shoes
    template_name = './product_detail.html'