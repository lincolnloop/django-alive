import logging

from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.cache import caches
from django.db import connections

from . import HealthcheckFailure

log = logging.getLogger(__name__)


def check_database(query="SELECT 1", database="default"):
    try:
        with connections[database].cursor() as cursor:
            cursor.execute(query)
    except Exception:
        log.exception("{} database connection failed".format(database))
        raise HealthcheckFailure("database error")


def check_staticfile(filename):
    """Verify static file is reachable"""
    if not staticfiles_storage.exists(filename):
        log.error("Can't find %s in static files.", filename)
        raise HealthcheckFailure("static files error")


def check_cache(key="django-alive", cache="default"):
    try:
        caches[cache].get(key)
    except Exception:
        log.exception("{} cache connection failed".format(cache))
        raise HealthcheckFailure("cache error")
