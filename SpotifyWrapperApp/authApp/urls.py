from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),  # Set /auth/ to display the login form
    path('login/', views.login_view, name='login'),  # Optional: Keep this if /auth/login/ is needed
    path('register/', views.register_view, name='register'),  # Add this route for user registration
]
