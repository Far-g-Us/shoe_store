from django.urls import path
from .views import *
from . import views


urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('<slug:url>/<int:id>/', ProductDetailView.as_view(), name='product_detail'),
    path('<slug:url>/<int:id>/review/', ProductDetailReview.as_view(), name='create_review'),
    path('review/edit/<int:pk>/', ReviewUpdateView.as_view(), name='review_edit'),
    path('<slug:url>/<int:id>/review/<int:review_id>/delete/', DeleteProductReview.as_view(), name='review_delete'),
    path('<slug:url>/<int:id>/comment/', CommentCreateView.as_view(), name='create_comment'),
    path('comment/edit/<int:pk>/', CommentUpdateView.as_view(), name='comment_edit'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
    path('category/<slug:url>/', ProductListView.as_view(), name='product_by_category'),
    path('filter/<int:country_id>/<str:category>/<int:page>/', ProductListView.as_view(), name='product_by_filter'),
    path('create/', ProductCreateView.as_view(), name='product_create'),
    path('<slug:url>/<int:id>/delete/', ProductDeleteView.as_view(), name='product_delete'),
]