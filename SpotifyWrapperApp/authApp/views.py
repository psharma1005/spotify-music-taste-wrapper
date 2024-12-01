from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json



def login_view(request):
    if request.method == 'POST':

        data = json.loads(request.body)
        #username = request.POST['username']
        #password = request.POST['password']
        
        username = data.get("username")
        password = data.get("password")


        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({"success": True, "message": "Login successful"})  # Redirect to homepage after login
        else:
            messages.error(request, 'Invalid username or password.')
            return JsonResponse({"success": False, "message": "Login failed"})

    # Render the login page on GET request
    return render(request, 'authApp/login.html')

def register_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        #username = request.POST['username']
        #password = request.POST['password']
        #confirm_password = request.POST['confirm_password']

        username = data.get('username')
        password = data.get('password')
        confirm_password = data.get('reenter')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'authApp/register.html')

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return render(request, 'authApp/register.html')

        # Create the user
        user = User.objects.create_user(username=username, password=password)
        messages.success(request, 'Account created successfully! You can now log in.')
        return JsonResponse({"success": True, "message": "Registration successful"})  # Redirect to login page after successful registration

    return render(request, 'authApp/register.html')  # Render the registration form on GET