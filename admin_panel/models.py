from django.db import models  # type: ignore
from django.contrib.auth.models import AbstractUser, Group, Permission  # type: ignore


class AdminUser(AbstractUser):
    is_superadmin = models.BooleanField(default=True)

    # Add unique related_name to avoid conflicts
    groups = models.ManyToManyField(
        Group,
        related_name="adminuser_set",
        blank=True,
        help_text="The groups this admin belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="adminuser_permissions_set",
        blank=True,
        help_text="Specific permissions for this admin.",
        verbose_name="user permissions",
    )
