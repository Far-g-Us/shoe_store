from django.urls import path
from face.views import indexView
from .views import *

urlpatterns = [
    path('', indexView.as_view(), name='home'),
    path('cart/', cartView.as_view(), name='cart'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),
    path('contact/', contactView.as_view(), name='contact'),
]