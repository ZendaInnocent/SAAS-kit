from django.views.generic import CreateView
from django.urls import reverse_lazy

from accounts import forms


class UserRegistrationView(CreateView):
    form_class = forms.UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('accounts:login')
