from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from product.models import Shoes, DiscountProduct
from product.forms import ShoesForm

class ProductListView(ListView):
    model = Shoes
    fields = '__all__'
    context_object_name = 'shoes'
    template_name = 'product_list.html'

class ProductDetailView(DetailView):
    model = Shoes
    context_object_name = 'shoe'
    template_name = 'product_detail.html'

    def get_queryset(self):
        return Shoes.objects.all()

    def get_object(self):
        product_id = self.kwargs['product_id']
        return Shoes.objects.get(pk=product_id)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shoe = self.get_object()
        context['sizes'] = shoe.size.all()
        context['collections'] = shoe.collection.all()
        return context


class ProductCreateView(CreateView):
    model = Shoes
    form_class = ShoesForm
    template_name = 'product_create.html'
    success_url = reverse_lazy('product_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shoes'] = Shoes.objects.all()
        return context

class ProductDeleteView(DeleteView):
    model = Shoes
    template_name = 'product_confirm_delete.html'
    success_url = reverse_lazy('product_list')

    def get_object(self, queryset=None):
        product_id = self.kwargs.get('product_id')
        return Shoes.objects.get(id=product_id)