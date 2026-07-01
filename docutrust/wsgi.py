"""
WSGI config for the DocuTrust project.

Exposes the WSGI callable as a module-level variable named ``application``.
Used by traditional synchronous servers such as Gunicorn or uWSGI.
"""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "docutrust.settings")

application = get_wsgi_application()
