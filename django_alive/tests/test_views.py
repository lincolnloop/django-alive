from io import StringIO
import json

from django.test import TestCase
from django.urls import reverse

from .side_effects import bad_database_check, ERR_MSG

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch


class ViewTestCase(TestCase):
    def test_liveness(self):
        response = self.client.get(reverse("alive_alive"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode("utf8"), "ok")

    def test_healthcheck(self):
        response = self.client.get(reverse("alive_health"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content.decode("utf8")), {"healthy": True})

    def test_healtcheck_failed(self):

        with patch(
            "django_alive.checks.check_database", side_effect=bad_database_check
        ):
            response = self.client.get(reverse("alive_health"))
        self.assertEqual(response.status_code, 503)
        self.assertEqual(
            json.loads(response.content.decode("utf8")),
            {"healthy": False, "errors": [ERR_MSG]},
        )
