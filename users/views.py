from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages 
from .forms import CustomUserCreationForm, CustomAuthenticationForm

# Registration view
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_approved = False  # User needs admin approval before login
            user.save()
            messages.success(request, "Registration successful! Please wait for admin approval.")
            return redirect("index")  # Redirect to the homepage after successful registration
        else:
            print(form.errors)  # Debugging errors if form validation fails

    else:
        form = CustomUserCreationForm()

    return render(request, "users/register.html", {"form": form})
# Login view


# Logout view (No changes needed here)
def user_logout(request):
    logout(request)
    return redirect('index')

def index(request):
    return render(request, 'core/index.html')

def student_login_view(request):
    return render(request, 'users/student_login.html')  # Update path
