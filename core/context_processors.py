"""Template context processors shared across every DocuTrust page."""
from __future__ import annotations

from django.conf import settings
from django.http import HttpRequest


def site_context(request: HttpRequest) -> dict[str, object]:
    """Inject global branding and feature metadata into every template.

    Args:
        request: The current request (unused but required by Django's
            context-processor contract).

    Returns:
        A dictionary of values made available to all templates.
    """
    return {
        "SITE_NAME": "DocuTrust",
        "SITE_TAGLINE": "Enterprise Advanced RAG Platform with "
        "Automated Self-Correction",
        "SITE_DESCRIPTION": (
            "Upload your documents and get grounded, cited answers powered "
            "by a self-correcting multi-agent retrieval pipeline."
        ),
        "SUPPORTS_STREAMING": True,
        "DEBUG_MODE": settings.DEBUG,
    }
