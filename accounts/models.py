"""Data models for user profiles and preferences."""
from __future__ import annotations

from django.contrib.auth.models import User
from django.db import models

from core.models import TimeStampedModel


class Profile(TimeStampedModel):
    """Extended profile information attached one-to-one to a Django ``User``.

    A profile is created automatically for every user via a ``post_save``
    signal (see :mod:`accounts.signals`).
    """

    class Theme(models.TextChoices):
        """UI theme preference options."""

        LIGHT = "light", "Light"
        DARK = "dark", "Dark"

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True,
        help_text="Optional profile picture.",
    )
    organization = models.CharField(max_length=150, blank=True)
    job_title = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True, max_length=500)
    theme = models.CharField(
        max_length=10,
        choices=Theme.choices,
        default=Theme.LIGHT,
    )

    class Meta(TimeStampedModel.Meta):
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self) -> str:
        """Return a human-readable representation."""
        return f"Profile<{self.user.username}>"

    @property
    def display_name(self) -> str:
        """Return the best available display name for the user."""
        full_name = self.user.get_full_name()
        return full_name or self.user.username

    @property
    def initials(self) -> str:
        """Return up to two uppercase initials for avatar fallbacks."""
        source = self.user.get_full_name() or self.user.username
        parts = [p for p in source.split() if p]
        if not parts:
            return "U"
        if len(parts) == 1:
            return parts[0][:2].upper()
        return (parts[0][0] + parts[-1][0]).upper()
