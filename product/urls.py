from django.urls import path, include
from product.views import ProductListView, ProductDetailView, ProductCreateView, ProductDeleteView

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('products/<int:product_id>', ProductDetailView.as_view(), name='product_detail'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:product_id>/delete', ProductDeleteView.as_view(), name='product_delete'),
]