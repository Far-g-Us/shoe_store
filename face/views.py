from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from face.models import Face, Cart, Contact
from product.models import Category, Shoes


class indexView(ListView):
    model = Face
    fields = '__all__'
    template_name = 'index.html'

    def get_queryset(self):
        return Face.objects.all()

    def __init__(self, url=None):
        self.url = url

    def get_products(self):
        category = None
        categories = Category.objects.all()
        shoes = Shoes.objects.filter(available=True)

        if self.url:
            category = get_object_or_404(Category, url=self.url)
            shoes = shoes.filter(category=category)
            return {
                'category': category,
                'categories': categories,
                'shoes': shoes
            }

class cartView(ListView):
    model = Cart
    fields = '__all__'
    template_name = 'cart.html'

    def get_queryset(self):
        return Cart.objects.all()

class contactView(ListView):
    model = Contact
    fields = '__all__'
    template_name = 'contact.html'

    def get_queryset(self):
        return Contact.objects.all()

