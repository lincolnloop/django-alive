from django.test import TestCase
from django.utils.module_loading import import_string

from .. import checks

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch


class TestChecks(TestCase):
    def test_database(self):
        self.assertIsNone(checks.check_database())

    def test_database_failed(self):
        with patch("django.db.connection.cursor", return_value=None):
            self.assertRaises(checks.HealthcheckFailure, checks.check_database)

    def test_staticfiles(self):
        self.assertIsNone(checks.check_staticfile("dummy.css"))

    def test_staticfiles_failed(self):
        with self.assertRaises(checks.HealthcheckFailure):
            checks.check_staticfile("does-not=exist.css")

    def test_cache(self):
        self.assertIsNone(checks.check_cache())

    def test_cache_failed(self):
        def broken_get(*args, **kwargs):
            raise ValueError

        with patch(
            "django.core.cache.backends.locmem.LocMemCache.get", side_effect=broken_get
        ):
            self.assertRaises(checks.HealthcheckFailure, checks.check_cache)

    def test_migrations(self):
        def migration_plan(*args, **kwargs):
            return [
                (
                    import_string(
                        "django.contrib.contenttypes.migrations.0001_initial.Migration"
                    ),
                    False,
                )
            ]

        with patch(
            "django.db.migrations.executor.MigrationExecutor.migration_plan",
            return_value=migration_plan,
        ):
            self.assertRaises(checks.HealthcheckFailure, checks.check_migrations)
