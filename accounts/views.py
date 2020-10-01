from django.shortcuts import get_object_or_404
from django.views.generic import CreateView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from accounts import forms
from main.models import Plan, Subscription

User = get_user_model()


class UserRegistrationView(CreateView):
    form_class = forms.UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        user_plan = self.request.GET.get('plan', 'Basic')
        plan = get_object_or_404(Plan, name=user_plan)
        user = User.objects.get(email=form.instance)
        Subscription.objects.create(user=user, plan=plan)
        return response
