from io import StringIO

from django.test import TestCase
from django.core.management import call_command, CommandError

from .side_effects import bad_database_check, ERR_MSG

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch


class CommandTestCase(TestCase):
    def test_command(self):
        out = StringIO()
        call_command("healthcheck", stdout=out)
        self.assertIn("OK", out.getvalue())

    def test_command_failed(self):
        err_msg = "database failed"
        out = StringIO()
        with patch(
            "django_alive.checks.check_database", side_effect=bad_database_check
        ):
            with self.assertRaises(CommandError):
                call_command("healthcheck")
