from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login
from .forms import AdminUserCreationForm

def register_admin(request):
    if request.method == 'POST':
        form = AdminUserCreationForm(request.POST)
        if form.is_valid():
            admin_user = form.save()
            login(request, admin_user)
            return redirect('admin_dashboard')  # Redirect to dashboard after registration
    else:
        form = AdminUserCreationForm()
    return render(request, 'admin_panel/admin_register.html', {'form': form})

from django.contrib.auth.decorators import login_required, user_passes_test

# Ensure only admins can access
def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password, backend='admin_panel.backends.AdminAuthBackend')
        
        if user is not None and user.is_superadmin: 
            login(request, user)
            return redirect('admin_dashboard')  # Redirect to admin dashboard
        else:
            return render(request, 'admin_panel/admin_login.html', {'error': 'Invalid credentials or not an admin'})
    
    return render(request, 'admin_panel/admin_login.html')

# Ensure only superadmins can access the dashboard
def is_admin(user):
    return user.is_superadmin

@login_required
@user_passes_test(is_admin)
def dashboard(request):
    return render(request, 'admin_panel/admin_dashboard.html')