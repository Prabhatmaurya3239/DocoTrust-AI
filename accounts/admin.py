"""Admin registration for profiles and an enriched user admin."""
from __future__ import annotations

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Profile


class ProfileInline(admin.StackedInline):
    """Edit a profile inline on the user admin page."""

    model = Profile
    can_delete = False
    verbose_name_plural = "Profile"
    fk_name = "user"
    readonly_fields = ("created_at", "updated_at")


class UserAdmin(BaseUserAdmin):
    """User admin augmented with the related profile."""

    inlines = (ProfileInline,)
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
        "date_joined",
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "date_joined")


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Standalone profile admin for quick lookups."""

    list_display = ("user", "organization", "job_title", "theme", "created_at")
    search_fields = ("user__username", "user__email", "organization")
    list_filter = ("theme",)
    readonly_fields = ("created_at", "updated_at")


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
