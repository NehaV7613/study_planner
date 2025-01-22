from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages 
from .forms import CustomUserCreationForm, CustomAuthenticationForm

# Registration view
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Explicitly specify the default backend for non-admin users
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            
            # Add a success message
            messages.success(request, 'Registration successful! You are now logged in.')
            return redirect('index')
        else:
            return render(request, 'users/register.html', {'form': form, 'errors': form.errors})
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

# Login view
def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            # Explicitly specify the default backend for non-admin users
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('index')
        else:
            return render(request, 'users/login.html', {'form': form})
    else:
        form = CustomAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

# Logout view (No changes needed here)
def user_logout(request):
    logout(request)
    return redirect('index')

def index(request):
    return render(request, 'core/index.html')
