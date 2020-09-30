from django.urls import path, include

from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.UserRegistrationView.as_view(), name='signup'),
    path('', include('django.contrib.auth.urls')),
]
