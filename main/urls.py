from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index_view, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('change-plan/', views.change_plan, name='change-plan'),
    path('confirm-plan/', views.confirm_plan, name='confirm-plan'),
    path('thank-you/', views.thank_you, name='thank-you'),
    path('payments/', views.payments, name='payments'),
]
