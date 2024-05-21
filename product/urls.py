from django.urls import path
from .views import *



urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('<slug:url>/<int:id>/', ProductDetailView.as_view(), name='product_detail'),
    path('<slug:url>/<int:id>/review/', ProductDetailReview.as_view(), name='create_review'),
    path('<slug:url>/<int:id>/review/<int:review_id>/delete/', DeleteProductReview.as_view(), name='review_delete'),
    path('category/<slug:url>/', ProductListView.as_view(), name='product_by_category'),
    path('create/', ProductCreateView.as_view(), name='product_create'),
    path('<slug:url>/<int:id>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('confirm/', ConfirmView.as_view(), name='product_confirm'),
]