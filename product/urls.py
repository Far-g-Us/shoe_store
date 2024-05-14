from django.urls import path
from .views import *

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('<slug:url>/<int:id>/', ProductDetailView.as_view(), name='product_detail'),
    path('category/<slug:url>/', ProductListView.as_view(), name='product_by_category'),
    path('create/', ProductCreateView.as_view(), name='product_create'),
    path('<int:id>/delete', ProductDeleteView.as_view(), name='product_delete'),
    path('confirm/', ConfirmView.as_view(), name='product_confirm'),
]