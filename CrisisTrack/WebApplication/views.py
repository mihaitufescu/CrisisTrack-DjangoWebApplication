from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required

# Home View
def index(request):
    return render(request, 'index.html', {
        'app_name': 'CrisisTrack',
        'app_description': 'A platform to report and manage cybersecurity incidents efficiently.'
    })

# Register View
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'authentification/register.html', {'form': form})

# Login View
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'authentification/login.html', {'error': 'Invalid username or password'})
    return render(request, 'authentification/login.html')

# Logout View
def user_logout(request):
    logout(request)
    return redirect('index')
