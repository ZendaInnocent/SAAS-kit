from django.shortcuts import render

from .models import Plan


def index_view(request):
    queryset = Plan.objects.all()
    context = {
        'plans': queryset,
    }
    return render(request, 'main/index.html', context)


def dashboard(request):
    return render(request, 'main/dashboard.html')
