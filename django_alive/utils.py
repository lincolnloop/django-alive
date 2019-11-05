from django.utils.module_loading import import_string

from . import HealthcheckFailure
from .settings import ALIVE_CHECKS


def perform_healthchecks():
    errors = []
    for func, kwargs in ALIVE_CHECKS.items():
        try:
            import_string(func)(**kwargs)
        except HealthcheckFailure as e:
            errors.append(str(e))
    return not errors, errors
