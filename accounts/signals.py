"""Signal handlers that keep profiles in sync with users."""
from __future__ import annotations

import logging

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile

logger = logging.getLogger("docutrust.accounts")


@receiver(post_save, sender=User)
def create_or_update_profile(
    sender: type[User], instance: User, created: bool, **kwargs: object
) -> None:
    """Create a :class:`Profile` for new users and persist it thereafter.

    Args:
        sender: The model class (``User``).
        instance: The user instance that was saved.
        created: Whether a new row was created.
        **kwargs: Additional signal keyword arguments (unused).
    """
    if created:
        Profile.objects.create(user=instance)
        logger.info("Created profile for new user '%s'", instance.username)
    else:
        # Ensure a profile always exists, even for users created before the
        # accounts app was installed.
        Profile.objects.get_or_create(user=instance)
