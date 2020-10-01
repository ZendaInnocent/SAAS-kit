from django.shortcuts import render

from .models import Plan
from django.contrib.auth.decorators import login_required


def index_view(request):
    queryset = Plan.objects.all()
    context = {
        'plans': queryset,
    }
    return render(request, 'main/index.html', context)


@login_required
def dashboard(request):
    return render(request, 'main/dashboard.html')
