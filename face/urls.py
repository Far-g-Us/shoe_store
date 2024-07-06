from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', indexView.as_view(), name='home'),
    path('cart/', cartView.as_view(), name='cart'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),
    path('update_cart/<int:product_id>/', update_cart, name='update_cart'),
    path('confirm/', ConfirmView.as_view(), name='confirm'),
    path('send-email/', send_email, name='send_email'),
    path('contact/', contactView.as_view(), name='contact'),
]