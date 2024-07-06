from django.urls import path
from .views import *


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView, name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('', ProfileView.as_view(), name='profile'),
    path('delete_user/<int:pk>/', DeleteUserProfile.as_view(), name='delete_user_confirm'),
    # path('', ProfileView.as_view(), name='profile'),
    # path('profile_update/', ProfileUpdateView.as_view(), name='profile_update'),
]