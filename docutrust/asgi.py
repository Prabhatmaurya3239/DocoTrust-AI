"""
ASGI config for the DocuTrust project.

Exposes the ASGI callable as a module-level variable named ``application``.
Used by asynchronous servers and enables streaming chat responses in later
modules.
"""
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "docutrust.settings")

application = get_asgi_application()
