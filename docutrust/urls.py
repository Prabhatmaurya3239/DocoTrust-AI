"""
Root URL configuration for the DocuTrust project.

Feature URLs are delegated to per-app URL modules as each module is built
(accounts, documents, chat, dashboard, rag, api). Module 1 wires up the
Django admin, the static/media handlers, and the ``core`` app that serves the
public landing page and health check.
"""
from __future__ import annotations

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "DocuTrust Administration"
admin.site.site_title = "DocuTrust Admin"
admin.site.index_title = "Enterprise RAG Platform Control Center"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("accounts/", include("accounts.urls")),
    path("documents/", include("documents.urls")),
    path("chat/", include("chat.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("api/", include("api.urls")),
]

# Serve uploaded media and collected static files during local development.
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.BASE_DIR / "static"
    )
