from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm, CustomAuthenticationForm

# Registration view (No changes needed here)
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'users/register.html', {'form': form, 'errors': form.errors})
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


# Login view
# Login view
def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
        else:
            # Pass the error message to the template
            error_message = "Invalid username or password."
            return render(request, 'users/login.html', {'form': form, 'error_message': error_message})
    else:
        form = CustomAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


# Logout view
def user_logout(request):
    logout(request)
    return redirect('index')
