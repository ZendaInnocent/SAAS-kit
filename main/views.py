from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.conf import settings

from portalsdk import APIContext, APIMethodType, APIRequest
from time import sleep

from main.mpesa import MPESA

from .models import Plan
from .forms import PaymentForm

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
        form = PaymentForm(request.POST)
        if form.is_valid():
            m_pesa = MPESA(api_key, public_key)

            parameters = {
                'input_Amount': 10,
                'input_Country': 'TZN',
                'input_Currency': 'TZS',
                # '000000000001',
                'input_CustomerMSISDN': request.POST.get('phone'),
                'input_ServiceProviderCode': '000000',
                'input_ThirdPartyConversationID':
                'asv02e5958774f7ba228d83d0d689761',
                'input_TransactionReference': 'T1234C',
                'input_PurchasedItemsDesc': 'Shoes',
            }

            results = m_pesa.c2b(parameters)

            if results.body['output_ResponseCode'] == 'INS-0':
                payment = form.save(commit=False)
                payment.user = request.user
                payment.phone = parameters['input_CustomerMSISDN']
                payment.amount = parameters['input_Amount']
                payment.transactionID = results.body['output_TransactionID']
                payment.conversationID = \
                    results.body['output_ConversationID']
                payment.third_convID = \
                    results.body['output_ThirdPartyConversationID']
                payment.save()

                messages.success(
                    request, 'Your Payment was Successfully sent!')

            else:
                messages.error(request, results.body['output_ResponseDesc'])

    return render(request, 'main/payments.html', {'form': PaymentForm()})
