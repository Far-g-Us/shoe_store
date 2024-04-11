from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from product.models import Shoes, Category
from decimal import Decimal
from product.forms import ShoesForm
from django.shortcuts import get_object_or_404


class ProductListView(ListView):
    model = Shoes
    fields = '__all__'
    context_object_name = 'shoes'
    template_name = 'product_list.html'

    def __init__(self, category_slug=None):
        self.category_slug = category_slug

    def get_object(self):
        return Shoes.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shoe = self.get_object()
        shoesList = []
        for item in shoe:
            price_decimal = Decimal(str(item.price))
            discount_decimal = Decimal(str(item.discount))
            discounted_price = price_decimal * (1 - discount_decimal / 100)
            item.price = {'price': price_decimal, 'sale': str(round(discounted_price))}
            shoesList.append(item)
            # print(shoesList)
        context['shoesList'] = shoesList
        return context

    def get_products(self):
        category = None
        categories = Category.objects.all()
        shoes = Shoes.objects.filter(available=True)

        if self.category_slug:
            category = get_object_or_404(Category, slug=self.category_slug)
            shoes = shoes.filter(category=category)
            return {
                'category': category,
                'categories': categories,
                'shoes': shoes
            }

class ProductDetailView(DetailView):
    model = Shoes
    context_object_name = 'shoe'
    template_name = 'product_detail.html'

    def __init__(self, id, slug):
        self.id = id
        self.slug = slug

    def get_product_detail(self):
        shoe = get_object_or_404(Shoes, id=self.id, slug=self.slug, available=True)
        return {'shoe': shoe}

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
        price_decimal = Decimal(str(shoe.price))
        discount_decimal = Decimal(str(shoe.discount))
        discounted_price = price_decimal * (1 - discount_decimal / 100)
        context['discounted_price'] = str(round(discounted_price))
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