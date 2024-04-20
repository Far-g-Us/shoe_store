from django.urls import path
from face.views import indexView
from .views import *

urlpatterns = [
    path('', indexView.as_view(), name='home'),
    path('cart/', cartView.as_view(), name='cart'),
    path('contact/', contactView.as_view(), name='contact'),
]