from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView, name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('', ProfileView.as_view(), name='profile'),
    path('delete_user/<int:pk>/', DeleteUserProfile.as_view(), name='delete_user_confirm'),
    # path('', ProfileView.as_view(), name='profile'),
    # path('profile_update/', ProfileUpdateView.as_view(), name='profile_update'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)