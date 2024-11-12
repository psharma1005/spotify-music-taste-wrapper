from django.urls import path
from .views import CustomLoginView, redirect_to_login

urlpatterns = [
    path('', redirect_to_login),  # Redirects `accounts/` to `accounts/login/`
    path('login/', CustomLoginView.as_view(), name='login'),
]
