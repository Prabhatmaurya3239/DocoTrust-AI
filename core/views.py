"""Views for the core app: public landing page and health check."""
from __future__ import annotations

import logging

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

logger = logging.getLogger("docutrust.core")

# Marketing feature grid rendered on the landing page. Kept in the view layer
# so it is trivially extendable without touching templates.
LANDING_FEATURES: list[dict[str, str]] = [
    {
        "icon": "bi-cloud-upload",
        "title": "Multi-Format Ingestion",
        "text": "Securely upload PDF, DOCX, and TXT files with drag & drop "
        "and instant validation.",
    },
    {
        "icon": "bi-diagram-3",
        "title": "Self-Correcting RAG",
        "text": "Retrieval, relevance grading, and query rewriting agents "
        "collaborate to ground every answer.",
    },
    {
        "icon": "bi-quote",
        "title": "Verifiable Citations",
        "text": "Every response is traced back to the exact source passages "
        "for full auditability.",
    },
    {
        "icon": "bi-lightning-charge",
        "title": "Streaming Answers",
        "text": "Watch responses render token by token with a polished "
        "typing animation.",
    },
    {
        "icon": "bi-graph-up-arrow",
        "title": "Analytics Dashboard",
        "text": "Track token usage, response times, and document statistics "
        "in real time.",
    },
    {
        "icon": "bi-shield-check",
        "title": "Enterprise Security",
        "text": "CSRF, XSS protection, secure uploads, and environment-driven "
        "secrets by default.",
    },
]

# High-level pipeline steps shown in the "How it works" section.
PIPELINE_STEPS: list[dict[str, str]] = [
    {"step": "01", "title": "Upload", "text": "Ingest your documents."},
    {"step": "02", "title": "Extract", "text": "Parse text with PyMuPDF."},
    {"step": "03", "title": "Embed", "text": "Vectorize semantic chunks."},
    {"step": "04", "title": "Retrieve", "text": "Find relevant passages."},
    {"step": "05", "title": "Grade", "text": "Score & rewrite if weak."},
    {"step": "06", "title": "Answer", "text": "Generate a cited response."},
]


def home(request: HttpRequest) -> HttpResponse:
    """Render the public landing page for DocuTrust.

    Args:
        request: The incoming HTTP request.

    Returns:
        The rendered landing page response.
    """
    logger.debug("Rendering landing page for %s", request.META.get("REMOTE_ADDR"))
    context = {
        "features": LANDING_FEATURES,
        "pipeline_steps": PIPELINE_STEPS,
    }
    return render(request, "core/home.html", context)


@require_GET
def health_check(request: HttpRequest) -> JsonResponse:
    """Lightweight liveness probe for monitoring and deployment checks.

    Args:
        request: The incoming HTTP request.

    Returns:
        A JSON payload describing service status.
    """
    return JsonResponse(
        {
            "status": "ok",
            "service": "docutrust",
            "version": "1.0.0",
        }
    )
