from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect, render
from django.template import context
from django.views.generic import CreateView, TemplateView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from accounts import forms
from main.models import Plan, Subscription
from .tokens import account_activation_token

User = get_user_model()


class UserRegistrationView(SuccessMessageMixin, CreateView):
    form_class = forms.UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('accounts:pending-registration')
    success_message = ('A confirmation email has been sent to your email'
                       '. Please confirm to finish registration.')

    def form_valid(self, form):
        response = super().form_valid(form)
        user_plan = self.request.GET.get('plan', 'Basic')
        plan = get_object_or_404(Plan, name=user_plan)
        user = User.objects.get(email=form.instance)
        # send confirmation email
        token = account_activation_token.make_token(user)
        user_id = urlsafe_base64_encode(force_bytes(user.id))
        url = 'http://localhost:8000' + reverse(
            'accounts:confirm-email', kwargs={'user_id': user_id,
                                              'token': token})
        message = get_template(
            'registration/account_activation_email.html').render(
            {'confirm_url': url})
        mail = EmailMessage(
            'Account Confirmation',
            message,
            to=[form.instance],
            from_email='noreply@domain.com')
        mail.content_subtype = 'html'
        mail.send()
        # create user subscription
        Subscription.objects.create(user=user, plan=plan)
        return response


class PendingRegistration(TemplateView):
    template_name = 'registration/registration_pending.html'


def confirm_registration_view(request, user_id, token):
    """View for user to confirm registration."""
    user_id = force_text(urlsafe_base64_decode(user_id))
    user = User.objects.get(pk=user_id)

    if user and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
    return redirect('accounts:login')


class UserLoginView(LoginView):
    # todo: get success url
    # registered user (Basic Plan) redirected to dashboard
    # registered user (Other Plans) redirected to payment options
    # superusers redirected to admin page

    pass
