"""Tests for the accounts app."""
from __future__ import annotations

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Profile


class ProfileSignalTests(TestCase):
    """Verify that a profile is auto-created for every user."""

    def test_profile_created_with_user(self) -> None:
        user = User.objects.create_user(username="alice", password="pw12345!")
        self.assertTrue(Profile.objects.filter(user=user).exists())

    def test_initials_property(self) -> None:
        user = User.objects.create_user(
            username="bob", first_name="Bob", last_name="Jones"
        )
        self.assertEqual(user.profile.initials, "BJ")


class AuthFlowTests(TestCase):
    """Exercise the registration and login flows end to end."""

    def test_register_creates_user_and_logs_in(self) -> None:
        response = self.client.post(
            reverse("register"),
            {
                "username": "carol",
                "first_name": "Carol",
                "last_name": "Smith",
                "email": "carol@example.com",
                "password1": "Str0ngPass!23",
                "password2": "Str0ngPass!23",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="carol").exists())

    def test_login_page_renders(self) -> None:
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sign in")
