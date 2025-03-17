from django.core.exceptions import PermissionDenied
from django.views.generic import View, DetailView, CreateView, DeleteView, FormView, UpdateView
from django_filters.views import FilterView
from django.contrib.auth.mixins import LoginRequiredMixin
from product.models import Shoes, Category, Review, CountryOfManufacture, Comment
from face.models import Cart, CartItem
from product.forms import ShoesForm, ReviewForm, CommentForm
from product.filters import ShoesFilter
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Count, Q, Prefetch
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, HttpResponse, JsonResponse
from django.urls import reverse_lazy, reverse
from urllib.parse import urlencode
from django.template.loader import render_to_string
from django.utils import timezone
import logging
logger = logging.getLogger(__name__)


class ProductListView(FilterView):
    model = Shoes
    filterset_class = ShoesFilter
    context_object_name = 'shoes'
    template_name = 'product_list.html'
    paginate_by = 6


    def get_queryset(self):
        queryset = super().get_queryset()

        print('Параметр сортировки:', self.request.GET.get('sort'))
        # Сортировка
        sort = self.request.GET.get('sort')
        if sort == 'name_asc':
            queryset = queryset.order_by('name')
        elif sort == 'name_desc':
            queryset = queryset.order_by('-name')
        elif sort == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort == 'price_desc':
            queryset = queryset.order_by('-price')

        search_query = self.request.GET.get('q')

        # Фильтрация по поисковому запросу
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        # Фильтрация по скидке 25%+
        if self.request.GET.get('big_discount') == '1':
            queryset = queryset.filter(discount__gte=25)

        filter = ShoesFilter(self.request.GET, queryset=queryset)

        category_url = self.kwargs.get('url')
        if category_url:
            category = Category.objects.get(url=category_url)
            queryset = filter.qs.filter(category__in=category.get_descendants(include_self=True))

        country_id = self.kwargs.get('country_id')
        if country_id:
            queryset = queryset.filter(country_of_manufacture__id=country_id)
        queryset = queryset.annotate(num_products=Count('category__shoes'))
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
        context['search_query'] = self.request.GET.get('q', '')
        # Выбираем все товары
        context['show_products'] = Shoes.objects.all()[:12]
        # Выбираем только товары у которых есть скидка
        context['discounted_products'] = Shoes.objects.filter(discount__gt=0, available=True)[:9]
        # Добавляем товары с большой скидкой в контекст
        context['big_discount_products'] = Shoes.objects.filter(discount__gte=25, available=True)[:9]
        # Фильтрация товаров по значениям из файла filters.py
        context['filter'] = ShoesFilter(self.request.GET, queryset=self.get_queryset())
        context['countries'] = CountryOfManufacture.objects.all()
        context['selected_categories'] = self.request.GET.getlist('category')
        context['filter_params'] = self.request.GET.copy()
        context['categories'] = Category.objects.all()
        category_url = self.kwargs.get('url')
        if category_url:
            category = Category.objects.get(url=category_url)
            context['name'] = f'Обувь из категории: {category.name}'
        return context


class ProductDetailView(DetailView):
    model = Shoes
    template_name = 'product_detail.html'
    context_object_name = 'shoe'
    paginate_by = 4 # Количество комментариев на страницу
    review_paginate_by = 4  # Количество отзывов на страницу

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
                # Оптимизация для отзывов
                Prefetch(
                    'reviews',
                    queryset=Review.objects.select_related('user', 'star')
                ),
                # Оптимизация для комментариев
                Prefetch(
                    'comments',
                    queryset=Comment.objects.select_related('author')
                )
            ),
            url=slug,
            id=product_id
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shoe = self.get_object()

        comments = shoe.comments.filter(parent=None).order_by('-created_at')

        # Для первоначальной загрузки
        paginator = Paginator(comments, self.paginate_by)
        page = self.request.GET.get('page', 1)

        try:
            comments_page = paginator.page(page)
        except (PageNotAnInteger, EmptyPage):
            comments_page = paginator.page(1)

        # Пагинация для отзывов
        reviews = shoe.reviews.all().order_by('-created_at')
        paginator_reviews = Paginator(reviews, self.review_paginate_by)
        page_reviews = self.request.GET.get('page_reviews', 1)

        try:
            reviews_page = paginator_reviews.page(page_reviews)
        except (PageNotAnInteger, EmptyPage):
            reviews_page = paginator_reviews.page(1)

        context['comments'] = comments_page
        context['reviews'] = reviews_page


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
            'discounted_products': Shoes.objects.filter(discount__gt=0, available=True)[:9],
            'num_comments': shoe.reviews.count(),
            'average_rating': shoe.average_rating,
            'stars': range(int(shoe.average_rating)) if shoe.average_rating else []
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

    def get(self, request, *args, **kwargs):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if is_ajax:
            # Определяем тип запроса
            reviews_page = request.GET.get('reviews_page')
            comments_page = request.GET.get('page')

            if reviews_page is not None:
                # Обработка AJAX для отзывов
                try:
                    page = int(reviews_page)
                    shoe = self.get_object()
                    reviews = shoe.reviews.all().order_by('-created_at')
                    paginator = Paginator(reviews, self.review_paginate_by)
                    page_obj = paginator.page(page)

                    html = render_to_string(
                        'reviews_partial.html',
                        {
                            'reviews': page_obj.object_list,
                            'user': request.user,
                            'shoe': shoe
                        }
                    )

                    return JsonResponse({
                        'html': html,
                        'has_next': page_obj.has_next(),
                        'next_page': page_obj.next_page_number() if page_obj.has_next() else None
                    })

                except Exception as e:
                    logger.error(f"Error in reviews AJAX handler: {str(e)}")
                    return JsonResponse({'error': str(e)}, status=500)

            elif comments_page is not None:
                # Обработка AJAX для комментариев
                try:
                    page = int(comments_page)
                    shoe = self.get_object()
                    comments = shoe.comments.filter(parent=None).order_by('-created_at')
                    paginator = Paginator(comments, self.paginate_by)
                    page_obj = paginator.page(page)

                    html = render_to_string(
                        'comments_partial.html',
                        {
                            'comments': page_obj.object_list,
                            'user': request.user
                        }
                    )

                    return JsonResponse({
                        'html': html,
                        'has_next': page_obj.has_next(),
                        'next_page': page_obj.next_page_number() if page_obj.has_next() else None
                    })

                except Exception as e:
                    logger.error(f"Error in comments AJAX handler: {str(e)}")
                    return JsonResponse({'error': str(e)}, status=500)

        return super().get(request, *args, **kwargs)


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
        review.shoes = shoes
        review.user = self.request.user
        review.save()
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


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'product_detail.html'

    def get_success_url(self):
        return reverse('product_detail', kwargs={
            'url': self.object.shoes.url,
            'id': self.object.shoes.id
        })

    def form_valid(self, form):
        form.instance.updated_at = timezone.now()
        response = super().form_valid(form)
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'text': self.object.text,
                'star': int(self.object.star.value)
            })
        return response


class DeleteProductReview(DeleteView):
    model = Review
    template_name = 'product_review_delete.html'

    def get_object(self, queryset=None):
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(Review, id=review_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        review = self.get_object()
        context['product'] = review.shoes
        return context

    def get_success_url(self):
        review = self.get_object()
        return reverse_lazy('product_detail', kwargs={
            'url': review.shoes.url,
            'id': review.shoes.id
        })


class CommentCreateView(LoginRequiredMixin, CreateView):
    form_class = CommentForm
    template_name = 'product_detail.html'

    def form_valid(self, form):
        shoe = get_object_or_404(Shoes, id=self.kwargs['id'])
        comment = form.save(commit=False)
        comment.shoes = shoe
        comment.author = self.request.user

        if not comment.author.image:
            comment.author.image = 'default_avatar.png'

        parent_id = form.cleaned_data.get('parent_id')
        if parent_id:
            comment.parent = get_object_or_404(Comment, id=parent_id)

        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('product_detail', kwargs={
            'url': self.kwargs['url'],
            'id': self.kwargs['id']
        }) + '#comments'


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'product_detail.html'

    def get_success_url(self):
        return reverse('product_detail', kwargs={
            'url': self.object.shoes.url,
            'id': self.object.shoes.id
        }) + f'#comment-{self.object.id}'

    def dispatch(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.author != request.user and not request.user.is_staff:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.updated_at = timezone.now()
        response = super().form_valid(form)
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'text': self.object.text,
                'updated_at': self.object.updated_at.strftime("%d %b %Y %H:%M")
            })
        return response


class CommentDeleteView(DeleteView):
    model = Comment
    template_name = 'product_comment_delete.html'
    pk_url_kwarg = 'pk'

    def dispatch(self, request, *args, **kwargs):
        comment = self.get_object()
        if not (request.user.is_staff or comment.author == request.user):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('product_detail', kwargs={
            'url': self.object.shoes.url,
            'id': self.object.shoes.id
        })