from django.views.generic import View, DetailView, CreateView, DeleteView, FormView
from django_filters.views import FilterView
from django.contrib.auth.mixins import LoginRequiredMixin
from product.models import Shoes, Category, Review, RatingStar, CountryOfManufacture
from face.models import Cart, CartItem
from product.forms import ShoesForm, ReviewForm
from product.filters import ShoesFilter
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Count
from django.contrib import messages
# from django.core.paginator import Paginator
from django.http import Http404, HttpResponse
from django.urls import reverse_lazy, reverse
from urllib.parse import urlencode


class ProductListView(FilterView):
    model = Shoes
    filterset_class = ShoesFilter
    context_object_name = 'shoes'
    template_name = 'product_list.html'
    paginate_by = 6


    def get_queryset(self):
        queryset = super().get_queryset()
        filter = ShoesFilter(self.request.GET, queryset=queryset)
        category_url = self.kwargs.get('url')
        if category_url:
            category = Category.objects.get(url=category_url)
            queryset = filter.qs.filter(category__in=category.get_descendants(include_self=True))
        country_id = self.kwargs.get('country_id')
        if country_id:
            queryset = queryset.filter(country_of_manufacture__id=country_id)
        queryset = queryset.annotate(num_products=Count('category__shoes')).order_by('id')
        ##------------------------------------------------------##
        price_min = self.request.GET.get('price__gte')
        price_max = self.request.GET.get('price__lte')

        if (price_min and price_max):
            queryset = queryset.filter(price__range=(price_min, price_max))
        elif price_min:
            queryset = queryset.filter(price__gte=price_min)
        elif price_max:
            queryset = queryset.filter(price__lte=price_max)
        # print(f'price_min: {price_min}, price_max: {price_max}')
        ##------------------------------------------------------##
        return queryset

    def get_context_data(self, **kwargs):
        ##------------------------------------------------------##
        # print(self.request.GET)
        context = super().get_context_data(**kwargs)
        # Обработка товаров для пагинации
        # shoes = context['shoes']
        paginator = context['paginator']
        page_obj = context['page_obj']
        page_numbers = [n for n in paginator.page_range if n > page_obj.number - 4 and n < page_obj.number + 4]
        context['page_numbers'] = page_numbers
        ##------------------------------------------------------##
        # Добавление параметров фильтрации в URL-адрес
        filter_params = self.request.GET.copy()
        filter_params._mutable = True
        filter_params.pop('page', None)
        context['filter_params'] = urlencode(filter_params)
        # Выбираем все товары
        context['show_products'] = Shoes.objects.all()[:12]
        # Выбираем только товары у которых есть скидка
        context['discounted_products'] = Shoes.objects.filter(discount__gt=0, available=True)[:9]
        # Фильтрация товаров по значениям из файла filters.py
        context['filter'] = ShoesFilter(self.request.GET, queryset=self.get_queryset())
        context['countries'] = CountryOfManufacture.objects.all()
        context['categories'] = Category.objects.all()
        category_url = self.kwargs.get('url')
        if category_url:
            category = Category.objects.get(url=category_url)
            context['name'] = f'Обувь из категории: {category.name}'
        return context


# class ProductByCategoryListView(ListView):
#     model = Shoes
#     template_name = 'product_list.html'
#     context_object_name = 'shoes'
#     category = None
#
#     def get_queryset(self):
#         self.category = Category.objects.get(url=self.kwargs['url'])
#         queryset = Shoes.objects.all().filter(category__url=self.category.url)
#         return queryset
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['name'] = f'Обувь из категории: {self.category.name}'
#         return context


class ProductDetailView(DetailView):
    model = Shoes
    template_name = 'product_detail.html'
    context_object_name = 'shoe'

    def get_queryset(self):
        return Shoes.objects.all()

    def get_object(self, queryset=None):
        slug = self.kwargs.get('url')
        product_id = self.kwargs.get('id')

        return get_object_or_404(
            Shoes.objects
            .select_related('category')  # Оптимизация для ForeignKey
            .prefetch_related(
                'brand',
                'gender',
                'color',
                'size',
                'collection',
                'upper_material',
                'lining_material',
                'outsole_material',
                'insole_material',
                'country_of_manufacture',
                'review_set__user',
                'review_set__star'
            ),
            url=slug,
            id=product_id
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shoe = self.get_object()

        # Все связи уже загружены через prefetch_related
        context.update({
            'brand_of_manufacture': shoe.brand.all(),
            'gender': shoe.gender.all(),
            'colors': shoe.color.all(),
            'sizes': shoe.size.all(),
            'collections': shoe.collection.all(),
            'upper_material': shoe.upper_material.all(),
            'lining_material': shoe.lining_material.all(),
            'outsole_material': shoe.outsole_material.all(),
            'insole_material': shoe.insole_material.all(),
            'country_of_manufacture': shoe.country_of_manufacture.all(),
            'num_comments': shoe.review_set.count(),
            'average_rating': shoe.average_rating,
            'stars': range(int(shoe.average_rating)) if shoe.average_rating else [],
            'discounted_products': Shoes.objects.filter(discount__gt=0, available=True)[:9]
        })

        # Оптимизированный запрос для статистики рейтингов
        rating_stats = (
            Review.objects
            .filter(shoes=shoe)
            .values('star__value')
            .annotate(count=Count('id'))
        )

        rating_dict = {stat['star__value']: stat['count'] for stat in rating_stats}
        context['rating_distribution'] = [
            {'stars': i, 'count': rating_dict.get(i, 0)}
            for i in range(5, 0, -1)
        ]
        context['has_ratings'] = sum(rating_dict.values()) > 0

        return context


class AddToCartView(LoginRequiredMixin, View):
    login_url = 'home'

    def post(self, request, *args, **kwargs):
        product_id = self.kwargs.get('product_id')
        shoes = get_object_or_404(Shoes, id=product_id)
        quantity = int(request.POST.get('quantity', 1))

        # Валидация количества
        if quantity < 1 or quantity > 10:
            messages.error(request, "Некорректное количество (допустимо от 1 до 10)")
            return redirect('product_detail', url=shoes.url, pk=shoes.id)

        # Логика добавления в корзину
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            shoes=shoes,
            user=request.user,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return redirect('cart')

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
    # success_url = reverse_lazy('product_list')

    def get_queryset(self):
        return Shoes.objects.all()

    def get_object(self, queryset=None):
        slug = self.kwargs.get('url')
        product_id = self.kwargs.get('id')
        try:
            return get_object_or_404(Shoes, url=slug, id=product_id)
        except Shoes.DoesNotExist:
            raise Http404("Product does not exist")

    def get_success_url(self):
        return reverse_lazy('product_list')

class ProductDetailReview(FormView):
    template_name = 'product_detail.html'
    form_class = ReviewForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        return kwargs

    def form_valid(self, form):
        shoes = self.get_object()
        review = form.save(commit=False)
        review.shoes = shoes  # Привязываем товар
        review.user = self.request.user  # Привязываем пользователя
        review.save()  # Сохраняем с звездой из формы
        return super().form_valid(form)

    def get_success_url(self):
        url = self.kwargs.get('url')
        product_id = self.kwargs.get('id')
        return reverse_lazy('product_detail', kwargs={'url': url, 'id': product_id})

    def get_object(self, queryset=None):
        url = self.kwargs.get('url')
        product_id = self.kwargs.get('id')
        try:
            return get_object_or_404(Shoes, url=url, id=product_id)
        except Shoes.DoesNotExist:
            raise Http404("Product does not exist")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shoe = self.get_object()
        context['shoe'] = shoe
        # Обновляем расчет среднего рейтинга
        avg_rating = shoe.average_rating
        context['stars'] = range(int(avg_rating)) if avg_rating > 0 else []
        return context

class DeleteProductReview(DeleteView):
    model = Review
    template_name = 'product_review_delete.html'
    # success_url = reverse_lazy('product_list')

    def get_queryset(self):
        return Review.objects.all()

    def get_object(self, queryset=None):
        review_id = self.kwargs.get('review_id')
        try:
            return get_object_or_404(Review, id=review_id)
        except Review.DoesNotExist:
            raise Http404("Comment does not exist")

    def get_success_url(self):
        product_url = self.kwargs.get('url')
        product_id = self.kwargs.get('id')
        return reverse_lazy('product_detail', kwargs={'url': product_url, 'id': product_id})


