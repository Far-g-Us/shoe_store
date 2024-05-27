from django.shortcuts import render
from django.views.generic import FormView, CreateView, ListView
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from .models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin


class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'login.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')



    def form_valid(self, form):
        user = form.save(commit=False)
        user.birth_date = form.cleaned_data.get('birth_date')
        user.full_name = form.cleaned_data.get('full_name')
        user.email = form.cleaned_data.get('email')
        user.image = form.cleaned_data.get('image')
        user.save()
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return reverse_lazy('login')
        else:
            return render(request, self.template_name, {'form': form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class UserProfileView(LoginRequiredMixin, ListView):
    pass
