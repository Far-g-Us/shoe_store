from django.urls import path, include
from product.views import ProductListView

urlpatterns = [
    path('', ProductListView.as_view(), name='product-category'),
]