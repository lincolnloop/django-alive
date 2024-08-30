import json

from django.test import TestCase, override_settings
from django.urls import reverse

from .side_effects import ERR_MSG, bad_database_check

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

    @override_settings(ALIVE_CHECKS={"django_alive.checks.check_migrations": {}})
    def test_deprecated_dict_format(self):
        with self.assertWarns(DeprecationWarning):
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
