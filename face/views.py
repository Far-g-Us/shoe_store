from django.views.generic import ListView, DetailView
from face.models import Face, Cart, Contact, Confirm
from product.models import Shoes
from face.models import Cart, CartItem
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib import messages


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
        latest_products = Shoes.objects.order_by('-created_at')[:6]

        # Выбираем только товары, не доступные для продажи
        available_products = Shoes.objects.filter(available=False)[:6]

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

    # def get_products(self):
    #     category = None
    #     categories = Category.objects.all()
    #     shoes = Shoes.objects.filter(available=True)
    #
    #     if self.url:
    #         category = get_object_or_404(Category, url=self.url)
    #         shoes = shoes.filter(category=category)
    #         return {
    #             'category': category,
    #             'categories': categories,
    #             'shoes': shoes
    #         }


class cartView(ListView):
    model = CartItem
    fields = '__all__'
    template_name = 'cart.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return CartItem.objects.filter(cart=cart)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        context['cart'] = cart
        cart_item_id = kwargs.get('cart_item_id')
        if cart_item_id:
            context['cart_item'] = CartItem.objects.get(id=cart_item_id)
        # добавляем эти строчки кода
        for cart_item in context['cart_items']:
            cart_item.total_price = cart_item.get_total_price
        return context


def add_to_cart(request, product_id):
    shoes = get_object_or_404(Shoes, id=product_id)
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, shoes=shoes, user=request.user)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        else:
            cart_item.quantity = 1
            cart_item.save()
        messages.success(request, 'Товар успешно добавлен в корзину')
        return redirect('cart')
    else:
        messages.info(request, 'Войдите в свой аккаунт, чтобы добавить товар в корзину')
        return redirect('home')


def update_cart(request, product_id):
    shoes = Shoes.objects.get(id=product_id)
    cart = Cart.objects.get(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, shoes=shoes)

    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        if quantity:
            cart_item.quantity = int(quantity)
            cart_item.save()

    context = {'cart': cart}
    return render(request, 'cart.html', context)


def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')
# def remove_from_cart(request, cart_item_id):
#     cart_item = CartItem.objects.get(id=cart_item_id)
#     cart_item.delete()
#     return redirect('cart')


class contactView(ListView):
    model = Contact
    fields = '__all__'
    template_name = 'contact.html'

    def get_queryset(self):
        return Contact.objects.all()


class ConfirmView(DetailView):
    model = CartItem
    fields = '__all__'
    template_name = 'confirm.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return CartItem.objects.filter(cart=cart)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        context['cart'] = cart
        # добавляем эти строчки кода
        for cart_item in context['cart_items']:
            cart_item.total_price = cart_item.get_total_price
        return context

    def post(self, request, *args, **kwargs):
        cart, created = Cart.objects.get_or_create(user=request.user)
        # создаем объект заказа
        confirm = Confirm.objects.create(user=request.user, cart=cart)
        # очищаем корзину
        cart.clear()
        # перенаправляем пользователя на страницу с подтверждением заказа
        return redirect('confirm', pk=confirm.pk)