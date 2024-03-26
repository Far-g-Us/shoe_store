from django.urls import path
from face.views import indexView

urlpatterns = [
    path('', indexView.as_view(), name='home'),
]