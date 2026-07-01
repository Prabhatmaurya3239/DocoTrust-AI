"""Views for registration, login/logout, and profile management."""
from __future__ import annotations

import logging

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .forms import (
    LoginForm,
    ProfileUpdateForm,
    RegisterForm,
    UserUpdateForm,
)

logger = logging.getLogger("docutrust.accounts")


def register(request: HttpRequest) -> HttpResponse:
    """Register a new user and sign them in on success."""
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            logger.info("New user registered: %s", user.username)
            messages.success(
                request, f"Welcome to DocuTrust, {user.first_name}!"
            )
            return redirect("dashboard")
        messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})


class DocuTrustLoginView(LoginView):
    """Session login using the styled :class:`LoginForm`."""

    template_name = "accounts/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def form_valid(self, form: LoginForm) -> HttpResponse:
        messages.success(
            self.request, f"Welcome back, {form.get_user().username}!"
        )
        logger.info("User logged in: %s", form.get_user().username)
        return super().form_valid(form)


class DocuTrustLogoutView(LogoutView):
    """Log out and redirect to the landing page."""

    next_page = reverse_lazy("home")


@login_required
def profile(request: HttpRequest) -> HttpResponse:
    """Display and update the current user's profile."""
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated.")
            logger.info("Profile updated for %s", request.user.username)
            return redirect("profile")
        messages.error(request, "Please correct the errors below.")
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {"user_form": user_form, "profile_form": profile_form}
    return render(request, "accounts/profile.html", context)


class DocuTrustPasswordChangeView(PasswordChangeView):
    """Allow authenticated users to change their password."""

    template_name = "accounts/password_change.html"
    success_url = reverse_lazy("profile")

    def form_valid(self, form: object) -> HttpResponse:
        messages.success(self.request, "Your password has been changed.")
        return super().form_valid(form)


class DocuTrustPasswordResetView(PasswordResetView):
    """Start the forgot-password flow."""

    template_name = "accounts/password_reset.html"
    email_template_name = "accounts/password_reset_email.html"
    subject_template_name = "accounts/password_reset_subject.txt"
    success_url = reverse_lazy("password_reset_done")


class DocuTrustPasswordResetDoneView(PasswordResetDoneView):
    """Confirmation that a reset email has been sent."""

    template_name = "accounts/password_reset_done.html"


class DocuTrustPasswordResetConfirmView(PasswordResetConfirmView):
    """Set a new password from a reset link."""

    template_name = "accounts/password_reset_confirm.html"
    success_url = reverse_lazy("password_reset_complete")


class DocuTrustPasswordResetCompleteView(PasswordResetCompleteView):
    """Confirmation that the password was reset."""

    template_name = "accounts/password_reset_complete.html"
