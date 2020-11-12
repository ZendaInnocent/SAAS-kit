import time
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
from django.utils import timezone

from main.mpesa import MPESA

from .models import Plan, Subscription
from .forms import TransactionForm

api_key = settings.MPESA['API_KEY']
public_key = settings.MPESA['PUBLIC_KEY']


def index_view(request):
    queryset = Plan.objects.all()
    context = {
        'plans': queryset,
    }
    return render(request, 'main/index.html', context)


@login_required
def dashboard(request):
    context = {
        'current_plan': request.user.get_subscription(),
    }
    return render(request, 'main/dashboard.html', context)


@login_required
def change_plan(request):
    plans = Plan.objects.all()

    if request.method == 'POST':
        cur_plan = request.user.get_subscription()
        request.session['current-plan'] = cur_plan
        plan = request.POST['plan']
        request.session['plan'] = plan
        new_plan = get_object_or_404(Plan, name=plan)
        if cur_plan == plan:
            messages.info(
                request, (f'You are current subscribed to {cur_plan} plan. '
                          f'Please select different plan to change.'))
            return redirect(reverse('main:change-plan'))
        else:
            return redirect(reverse('main:confirm-plan'))

    context = {
        'plans': plans,
    }
    return render(request, 'main/change_plan.html', context)


@login_required
def confirm_plan(request):
    current_plan = request.session['current-plan']

    if request.method == 'POST':
        plan = request.session['plan'] if request.session['plan'] else None
        if plan != current_plan:
            new_plan = get_object_or_404(Plan, name=plan)
            # set new plan for the user
            if request.user.is_authenticated:
                user = request.user
                # get user subscription
                sub = user.subscription_set.first()
                sub.plan = new_plan
                sub.save()
                del request.session['plan']
                messages.success(
                    request, 'You plan has changed successful.')
            return redirect(reverse('main:thank-you'))

    context = {
        'current_plan': request.session['current-plan'],
        'new_plan': request.session['plan'],
    }
    return render(request, 'main/confirm_plan.html', context)


@login_required
def thank_you(request):
    new_plan = request.user.get_subscription()
    return render(request, 'main/thank_you.html', {'new_plan': new_plan})


@login_required
def payments(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            parameters = {}
            m_pesa = MPESA(api_key, public_key)
            results = m_pesa.c2b(parameters)

            if results.body['output_ResponseCode'] == 'INS-0':
                transaction = form.save(commit=False)
                transaction.subscrition = request.user.subscription_set.first()
                transaction.user = request.user
                transaction.phone = request.POST.get('phone')
                transaction.amount = request.user.subscription_set.first()\
                    .plan.price
                transaction.transactionID = results.body['output_TransactionID']
                transaction.conversationID = \
                    results.body['output_ConversationID']
                transaction.reference_no = reference_no
                transaction.save()

                return HttpResponse('Your Payment was Successfully sent!')

            elif results.body['output_ResponseCode'] == 'INS-1':
                messages.add_message(request, messages.ERROR, 'Internal Error')

            elif results.body['output_ResponseCode'] == 'INS-6':
                messages.add_message(
                    request, messages.ERROR, 'Transaction Failed')

            elif results.body['output_ResponseCode'] == 'INS-9':
                messages.add_message(
                    request, messages.ERROR, 'Request timeout')

            elif results.body['output_ResponseCode'] == 'INS-10':
                messages.add_message(
                    request, messages.ERROR, 'Duplicate Transaction')

            elif results.body['output_ResponseCode'] == 'INS-2006':
                messages.add_message(
                    request, messages.ERROR, 'Insufficient balance')

            else:
                messages.add_message(
                    request, messages.ERROR,
                    'Configuration Error, contact with support team')

    return render(request, 'main/payments.html', {'form': TransactionForm()})
