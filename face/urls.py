from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add_to_cart/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('remove_from_cart/<int:cart_item_id>/', RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('update_cart/<int:product_id>/', UpdateCartView.as_view(), name='update_cart'),
    path('confirm/', ConfirmView.as_view(), name='confirm'),
    path('contact/', ContactView.as_view(), name='contact'),
    #path('send-email/', send_email, name='send_email'),
]