"""Shared abstract models and mixins used across DocuTrust apps."""
from __future__ import annotations

from django.db import models


class TimeStampedModel(models.Model):
    """Abstract base model that adds self-managed timestamp fields.

    Concrete feature models (documents, chats, logs, etc.) inherit from this
    mixin to avoid duplicating created/updated bookkeeping.
    """

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]
