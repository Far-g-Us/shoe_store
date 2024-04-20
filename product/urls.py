from django.urls import path, include
from product.views import ProductListView, ProductDetailView, ProductCreateView, ProductDeleteView
from .views import *

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    # path('<category_slug>/', ProductListView.as_view(), name='product_list_by_category'),
    path('<int:product_id>/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    # path('<id>/<slug>/', ProductDetailView.as_view(), name='product_detail_by_category'),
    path('create/', ProductCreateView.as_view(), name='product_create'),
    path('<int:product_id>/delete', ProductDeleteView.as_view(), name='product_delete'),
    path('confirm/', confirmView.as_view(), name='confirm'),
]