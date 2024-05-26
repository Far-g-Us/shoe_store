from django.views.generic import ListView
from reguser.models import Profile


class LoginView(ListView):
    # model = Profile
    template_name = 'login.html'

