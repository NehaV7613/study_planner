from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from users.models import CustomUser  # Import the existing user model
from .models import ApprovalRequest
from .forms import AdminUserCreationForm
from .models import Syllabus
from .forms import SyllabusUploadForm


# Ensure only superadmins can access certain views
def is_superadmin(user):
    return user.is_superadmin  # Use the correct field

# Admin registration (Only superadmins can register new admins)
@login_required
@user_passes_test(is_superadmin)
def register_admin(request):
    if request.method == 'POST':
        form = AdminUserCreationForm(request.POST)
        if form.is_valid():
            admin_user = form.save(commit=False)
            admin_user.is_superadmin = True  # Ensure the new user is an admin
            admin_user.save()
            messages.success(request, "New admin registered successfully!")
            return redirect('admin_dashboard')  
    else:
        form = AdminUserCreationForm()
    
    return render(request, 'admin_panel/admin_register.html', {'form': form})

# Admin login
def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)  # Added password

        if user is not None and user.is_superadmin: 
            login(request, user)
            return redirect('admin_dashboard')  
        else:
            return render(request, 'admin_panel/admin_login.html', {'error': 'Invalid credentials or not an admin'})
    
    return render(request, 'admin_panel/admin_login.html')

# Admin dashboard (Only accessible to superadmins)
@login_required
@user_passes_test(is_superadmin)
def dashboard(request):
    return render(request, 'admin_panel/admin_dashboard.html')

# Approve or reject pending users
@login_required(login_url='/admin_panel/login/')  # Redirect to admin login
@user_passes_test(is_superadmin)  # Restrict to superadmins
def approve_users(request):
    # Fetch users who are not yet approved
    pending_users = CustomUser.objects.filter(is_approved=False)

    if request.method == "POST":
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')
        user = get_object_or_404(CustomUser, id=user_id)

        if action == "approve":
            user.is_approved = True  # Approve user
            user.is_active = True  # Activate user
            user.save()
            messages.success(request, f"{user.username} has been approved!")
        elif action == "reject":
            user.delete()  # Delete user if rejected
            messages.error(request, f"{user.username} has been rejected and removed!")

        return redirect(request.path)  # Reload the same page instead of redirecting

    return render(request, 'admin_panel/approve_users.html', {'pending_users': pending_users})


@login_required
@user_passes_test(is_superadmin)
def upload_syllabus(request):
    if request.method == "POST":
        form = SyllabusUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Syllabus uploaded successfully!")
            return redirect("syllabus_list")
    else:
        form = SyllabusUploadForm()
    return render(request, "admin_panel/upload_syllabus.html", {"form": form})


@login_required
@user_passes_test(is_superadmin)
def syllabus_list(request):
    syllabi = Syllabus.objects.all()
    return render(request, "admin_panel/syllabus_list.html", {"syllabi": syllabi})
