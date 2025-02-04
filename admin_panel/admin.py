from django.contrib import admin

# Register your models here.
from .models import ApprovalRequest
from users.models import CustomUser

@admin.register(ApprovalRequest)
class ApprovalRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'requested_at')

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'role', 'is_approved')
    list_filter = ('role', 'is_approved')
    actions = ['approve_users', 'reject_users']

    def approve_users(self, request, queryset):
        queryset.update(is_approved=True)
        ApprovalRequest.objects.filter(user__in=queryset).delete()  # Remove requests on approval
        self.message_user(request, "Selected users have been approved.")

    def reject_users(self, request, queryset):
        queryset.delete()
        self.message_user(request, "Selected users have been rejected.")