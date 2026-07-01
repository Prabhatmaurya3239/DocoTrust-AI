"""Smoke tests for the core app."""
from __future__ import annotations

from django.test import TestCase
from django.urls import reverse


class CorePagesTests(TestCase):
    """Verify that the foundational pages respond correctly."""

    def test_landing_page_renders(self) -> None:
        """The landing page returns HTTP 200 and includes the brand name."""
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "DocuTrust")

    def test_health_check_returns_ok(self) -> None:
        """The health endpoint returns a JSON ok status."""
        response = self.client.get(reverse("health_check"))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {"status": "ok", "service": "docutrust", "version": "1.0.0"},
        )
