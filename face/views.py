from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from face.models import Face, Cart, Contact
from product.models import Category, Shoes
#from decimal import Decimal


class indexView(ListView):
    model = Face
    fields = '__all__'
    template_name = 'index.html'
    context_object_name = 'shoes'




    def __init__(self, url=None):
        self.url = url

    def get_object(self):
        return Shoes.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Выбираем последние добавленные товары
        latest_products = Shoes.objects.order_by('-created_at')[:12]

        # Выбираем только товары, доступные для продажи
        available_products = Shoes.objects.filter(available=False)[:12]

        # Выбираем только товары у которых есть скидка
        discounted_products = Shoes.objects.filter(discount__gt=0, available=True)[:9]
        # shoe = self.get_object()
        # shoesList = []
        # for item in shoe:
        #     price_decimal = Decimal(str(item.price))
        #     discount_decimal = Decimal(str(item.discount))
        #     discounted_price = price_decimal * (1 - discount_decimal / 100)
        #     item.price = {'price': price_decimal, 'sale': str(round(discounted_price))}
        #     shoesList.append(item)
        #     # print(shoesList)
        # context['shoesList'] = shoesList
        context['latest_products'] = latest_products
        context['available_products'] = available_products
        context['discounted_products'] = discounted_products
        return context

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

