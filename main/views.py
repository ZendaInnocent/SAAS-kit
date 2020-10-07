from django.contrib.auth import login
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse

from .models import Plan


def index_view(request):
    queryset = Plan.objects.all()
    context = {
        'plans': queryset,
    }
    return render(request, 'main/index.html', context)


@login_required
def dashboard(request):
    context = {
        'current_plan': request.user.subscription_set.first(),
    }
    return render(request, 'main/dashboard.html', context)


@login_required
def change_plan(request):
    plans = Plan.objects.all()

    if request.method == 'POST':
        sub = request.user.subscription_set.first()
        plan = request.POST['plan']
        request.session['plan'] = plan
        new_plan = get_object_or_404(Plan, name=plan)
        if sub.plan == new_plan:
            messages.info(
                request, (f'You are current subscribed to {sub.plan} plan. '
                          f'Please select different plan to change.'))
            return redirect(reverse('main:change-plan'))
        else:
            context = {'new_plan': new_plan, 'current_plan': sub.plan}
            return render(request, 'main/confirm_plan.html', context)

    context = {
        'plans': plans,
    }
    return render(request, 'main/change_plan.html', context)


@login_required
def confirm_plan(request):
    if request.method == 'POST':
        current_plan = request.user.subscription_set.first()
        plan = request.session['plan'] if request.session['plan'] else None
        if plan != current_plan.plan:
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
            return render(request, 'main/thank_you.html', {
                'new_plan': new_plan,
            })

    context = {
        'current_plan': request.user.subscription_set.first(),
    }
    return render(request, 'main/confirm_plan.html', context)


@login_required
def thank_you(request):
    return render(request, 'main/thank_you.html')


@login_required
def payments(request):
    return render(request, 'main/payments.html')
