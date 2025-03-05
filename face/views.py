from django.views.generic import ListView, View
from face.models import Face, Contact, Cart, CartItem
from product.models import Shoes
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse



class IndexView(ListView):
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
        latest_products = Shoes.objects.order_by('-created_at')[:9]

        # Выбираем только товары, не доступные для продажи
        available_products = Shoes.objects.filter(available=False)[:9]

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


class CartView(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = CartItem
    template_name = 'cart.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return cart.cartitem_set.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        context['cart'] = cart
        cart_item_id = kwargs.get('cart_item_id')
        if cart_item_id:
            context['cart_item'] = CartItem.objects.get(id=cart_item_id)
        for cart_item in context['cart_items']:
            cart_item.total_price = cart_item.get_total_price
        return context


class AddToCartView(LoginRequiredMixin, View):
    login_url = 'home'

    def get(self, request, *args, **kwargs):
        # Обработка GET-запросов (простые ссылки)
        return self.process_add_to_cart(request, quantity=1)

    def post(self, request, *args, **kwargs):
        # Обработка POST-запросов (формы с количеством)
        quantity = int(request.POST.get('quantity', 1))
        return self.process_add_to_cart(request, quantity)

    def process_add_to_cart(self, request, quantity):
        product_id = self.kwargs.get('product_id')
        shoes = get_object_or_404(Shoes, id=product_id)

        # Валидация количества
        if quantity < 1 or quantity > 10:
            messages.error(request, "Некорректное количество (1-10)")
            return redirect('product_detail', url=shoes.url, pk=shoes.id)

        # Логика добавления в корзину
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            shoes=shoes,
            defaults={'user': request.user, 'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return redirect('cart')


class UpdateCartView(LoginRequiredMixin, View):
    login_url = 'login'

    def post(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')
        shoes = get_object_or_404(Shoes, id=product_id)
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItem, cart=cart, shoes=shoes)

        quantity = request.POST.get('quantity')
        if quantity and quantity.isdigit():
            cart_item.quantity = int(quantity)
            cart_item.save()
            messages.success(request, 'Количество успешно обновлено')
        else:
            messages.error(request, 'Некорректное количество')

        return redirect('cart')


class RemoveFromCartView(LoginRequiredMixin, View):
    login_url = 'login'

    def post(self, request, *args, **kwargs):
        cart_item_id = kwargs.get('cart_item_id')
        cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
        cart_item.delete()
        messages.success(request, 'Товар удален из корзины')
        return redirect('cart')


class ContactView(ListView):
    model = Contact
    fields = '__all__'
    template_name = 'contact.html'

    def get_queryset(self):
        return Contact.objects.all()


# class ConfirmView(DetailView):
#     model = CartItem
#     fields = '__all__'
#     template_name = 'confirm.html'


class ConfirmView(ListView):
    model = CartItem
    template_name = 'confirm.html'
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
        for cart_item in context['cart_items']:
            cart_item.total_price = cart_item.get_total_price
        return context


# def send_email(request):
#     if request.method == 'POST':
#         try:
#             recipient_email = request.POST.get('email')
#             subject = 'Подтверждение покупки'
#             message = 'Спасибо за вашу покупку! Мы подтвердили ее и свяжемся с вами в ближайшее время.'
#             from_email = settings.DEFAULT_FROM_EMAIL
#
#             # Добавьте логирование
#             print(f"Пытаемся отправить письмо на {recipient_email}")
#
#             send_mail(
#                 subject,
#                 message,
#                 from_email,
#                 [recipient_email],
#                 fail_silently=False,
#                 auth_user=settings.EMAIL_HOST_USER,
#                 auth_password=settings.EMAIL_HOST_PASSWORD
#             )
#             return JsonResponse({'success': True})
#
#         except Exception as e:
#             print(f"Ошибка отправки: {str(e)}")
#             return JsonResponse({'success': False, 'error': str(e)})
#
#     return JsonResponse({'success': False, 'error': 'Invalid method'})