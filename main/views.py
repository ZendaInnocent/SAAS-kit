import time
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
from django.utils import timezone

from .models import Plan, Subscription
from .forms import TransactionForm
from portalsdk import APIContext, APIMethodType, APIRequest


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
        transaction = TransactionForm(request.POST)
        transaction.amount = 5000
        transaction.save()
    return render(request, 'main/payments.html', {'form': TransactionForm()})
