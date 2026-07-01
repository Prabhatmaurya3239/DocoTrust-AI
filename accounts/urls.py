"""URL routes for authentication and profile management."""
from __future__ import annotations

from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.DocuTrustLoginView.as_view(), name="login"),
    path("logout/", views.DocuTrustLogoutView.as_view(), name="logout"),
    path("profile/", views.profile, name="profile"),
    path(
        "password/change/",
        views.DocuTrustPasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "password/reset/",
        views.DocuTrustPasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "password/reset/done/",
        views.DocuTrustPasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "password/reset/confirm/<uidb64>/<token>/",
        views.DocuTrustPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password/reset/complete/",
        views.DocuTrustPasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]
