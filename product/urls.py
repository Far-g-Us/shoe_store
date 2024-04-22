from django.urls import path
from .views import *

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('<int:id>/<slug:url>/', ProductDetailView.as_view(), name='product_detail'),
    # path('<id>/<slug>/', ProductDetailView.as_view(), name='product_detail_by_category'),
    path('create/', ProductCreateView.as_view(), name='product_create'),
    path('<int:product_id>/delete', ProductDeleteView.as_view(), name='product_delete'),
    path('confirm/', ConfirmView.as_view(), name='product_confirm'),
]