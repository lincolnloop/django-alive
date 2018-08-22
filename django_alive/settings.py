from django.conf import settings

DEFAULT_ALIVE_CHECKS = {"django_alive.checks.check_database": {}}
ALIVE_CHECKS = getattr(settings, "ALIVE_CHECKS", DEFAULT_ALIVE_CHECKS)
