import sys

from django.core.management import CommandError, call_command
from django.test import TestCase

from .side_effects import bad_database_check

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

# Python 2.7 support
if sys.version_info > (3, 0):
    from io import StringIO
else:
    from io import BytesIO as StringIO


class CommandTestCase(TestCase):
    def test_command(self):
        out = StringIO()
        call_command("healthcheck", stdout=out)
        self.assertIn("OK", out.getvalue())

    def test_command_failed(self):
        with patch(
            "django_alive.checks.check_database", side_effect=bad_database_check
        ):
            with self.assertRaises(CommandError):
                call_command("healthcheck")
