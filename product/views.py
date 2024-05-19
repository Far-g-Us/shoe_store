from django.views.generic import ListView, DetailView, CreateView, DeleteView, FormView
from django_filters.views import FilterView
from product.models import Shoes, Category, Confirm, Review
from product.forms import ShoesForm, ReviewForm
from product.filters import ShoesFilter
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Count
from django.core.paginator import Paginator
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse_lazy




class ProductListView(FilterView):
    model = Shoes
    filterset_class = ShoesFilter
    context_object_name = 'shoes'
    template_name = 'product_list.html'
    paginate_by = 9

    def get_queryset(self):
        queryset = super().get_queryset()
        filter = ShoesFilter(self.request.GET, queryset=queryset)
        category_url = self.kwargs.get('url')
        if category_url:
            category = Category.objects.get(url=category_url)
            queryset = filter.qs.filter(category__in=category.get_descendants(include_self=True))
        queryset = queryset.annotate(num_products=Count('category__shoes')).order_by('id')
        #### НЕ ТРОГАЙ ПОКА РАБОТАЕТ ####
        price_min = self.request.GET.get('price__gte')
        price_max = self.request.GET.get('price__lte')

        if (price_min and price_max):
            queryset = queryset.filter(price__range=(price_min, price_max))
        elif price_min:
            queryset = queryset.filter(price__gte=price_min)
        elif price_max:
            queryset = queryset.filter(price__lte=price_max)
        # print(f'price_min: {price_min}, price_max: {price_max}')
        ###################################
        return queryset

    def get_context_data(self, **kwargs):
        #### НЕ ТРОГАЙ ПОКА РАБОТАЕТ ####
        # print(self.request.GET)
        context = super().get_context_data(**kwargs)
        # Обработка товаров для пагинации
        # shoes = context['shoes']
        paginator = context['paginator']
        page_obj = context['page_obj']
        page_numbers = [n for n in paginator.page_range if n > page_obj.number - 4 and n < page_obj.number + 4]
        context['page_numbers'] = page_numbers
        #######################################
        # Выбираем все товары
        context['show_products'] = Shoes.objects.all()[:12]
        # Выбираем только товары у которых есть скидка
        context['discounted_products'] = Shoes.objects.filter(discount__gt=0, available=True)[:9]
        # Фильтрация товаров по значениям из файла filters.py
        context['filter'] = ShoesFilter(self.request.GET, queryset=self.get_queryset())
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
    


    # def __init__(self, id, url, *args, **kwargs):
    #     self.id = id
    #     self.url = url
    #     super().__init__(*args, **kwargs)
    #
    # def get(self, request):
    #     shoes = Shoes.objects.get(id=self.id)
    #     context = {
    #         'shoes': shoes,
    #         'url': self.url
    #     }
    #     return render(request, 'product_detail.html', context)

    def get_queryset(self):
        return Shoes.objects.all()

    def get_object(self, queryset=None):
        slug = self.kwargs.get('url')  # Используйте 'url' вместо 'slug'
        product_id = self.kwargs.get('id')  # Используйте 'id' вместо 'product_id'
        #print(product_id, slug)
        try:
            return get_object_or_404(Shoes, url=slug, id=product_id)
        except Shoes.DoesNotExist:
            raise Http404("Product does not exist")

    # def get_object(self):
    #     product_id = self.kwargs.get('product_id')
    #     try:
    #         return Shoes.objects.get(pk=product_id)
    #     except Shoes.DoesNotExist:
    #         raise Http404("Product does not exist")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shoe = self.get_object()
        context['gender'] = shoe.gender.all()
        context['colors'] = shoe.color.all()
        context['sizes'] = shoe.size.all()
        context['collections'] = shoe.collection.all()
        context['upper_material'] = shoe.upper_material.all()
        context['lining_material'] = shoe.lining_material.all()
        context['outsole_material'] = shoe.outsole_material.all()
        context['insole_material'] = shoe.insole_material.all()
        context['country_of_manufacture'] = shoe.country_of_manufacture.all()

        # Выбираем только товары у которых есть скидка
        # discounted_products = Shoes.objects.filter(discount__gt=0, available=True)[:9]
        # context['discounted_products'] = discounted_products
        context['discounted_products'] = Shoes.objects.filter(discount__gt=0, available=True)[:9]

        # price_decimal = Decimal(str(shoe.price))
        # discount_decimal = Decimal(str(shoe.discount))
        # discounted_price = price_decimal * (1 - discount_decimal / 100)
        # context['discounted_price'] = str(round(discounted_price))
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


class ConfirmView(DetailView):
    model = Confirm
    fields = '__all__'
    template_name = 'product_confirm.html'

    def get_queryset(self):
        return Shoes.objects.all()

    def get_object(self, queryset=None):
        product_id = self.kwargs.get('product_id')
        try:
            return Confirm.objects.get(id=product_id)
        except Confirm.DoesNotExist:
            product_id = None


# class AddReview(FormView):
#     def post(self, request, pk):
#         form = ReviewForm(request.POST)
        
#         shoes = Shoes.objects.get(pk)
#         if form.is_valid():
#             form = form.save(commit=False)
#             form.shoes = shoes
#             form.save()
#         return redirect(shoes.get_absolute_url())

class ProductDetailReview(FormView):
    template_name = 'product_detail.html'
    form_class = ReviewForm

    def form_valid(self, form):
        shoes = self.get_object()
        review = Review.objects.create(shoes=shoes, **form.cleaned_data)
        review.save()
        print(review)
        return super().form_valid(form)

    def get_object(self, queryset=None):
        url = self.kwargs.get('url')
        product_id = self.kwargs.get('id')
        try:
            return get_object_or_404(Shoes, url=url, id=product_id)
        except Shoes.DoesNotExist:
            raise Http404("Product does not exist")

    def get_success_url(self):
        url = self.kwargs.get('url')
        product_id = self.kwargs.get('id')
        return reverse_lazy('product_detail', kwargs={'url': url, 'id': product_id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shoes'] = self.get_object()
        return context