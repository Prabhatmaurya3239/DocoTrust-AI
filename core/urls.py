"""URL routing for the core app."""
from __future__ import annotations

from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("health/", views.health_check, name="health_check"),
]
