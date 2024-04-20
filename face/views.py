from django.views.generic import ListView, DetailView
from face.models import Face, Cart, Contact


class indexView(ListView):
    model = Face
    fields = '__all__'
    template_name = 'index.html'

    def get_queryset(self):
        return Face.objects.all()

class cartView(ListView):
    model = Cart
    fields = '__all__'
    template_name = 'cart.html'

    def get_queryset(self):
        return Cart.objects.all()

class contactView(ListView):
    model = Contact
    fields = '__all__'
    template_name = 'contact.html'

    def get_queryset(self):
        return Contact.objects.all()