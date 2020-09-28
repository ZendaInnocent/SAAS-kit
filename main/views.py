from django.shortcuts import render


def index_view(request):

    return render(request, 'main/index.html')


def dashboard(request):
    return render(request, 'main/dashboard.html')
