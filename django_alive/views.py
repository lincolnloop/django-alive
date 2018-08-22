import logging

from django.http import HttpResponse, JsonResponse
from django.utils.module_loading import import_string

from . import HealthcheckFailure
from .settings import ALIVE_CHECKS

log = logging.getLogger(__name__)


def alive(request):
    return HttpResponse("ok")


def healthcheck(request):
    # Verify DB is connected
    errors = []
    for func, kwargs in ALIVE_CHECKS.items():
        try:
            import_string(func)(**kwargs)
        except HealthcheckFailure as e:
            errors.append(str(e))
    if errors:
        return JsonResponse({"healthy": False, "errors": errors}, status=503)

    return JsonResponse({"healthy": True})
