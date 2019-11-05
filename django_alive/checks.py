import logging

from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.cache import caches
from django.db import connections
from django.db.migrations.executor import MigrationExecutor

from . import HealthcheckFailure

log = logging.getLogger(__name__)


def check_database(query="SELECT 1", database="default"):
    try:
        with connections[database].cursor() as cursor:
            cursor.execute(query)
    except Exception:
        log.exception("%s database connection failed", database)
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
        log.exception("%s cache connection failed", cache)
        raise HealthcheckFailure("cache error")


def check_migrations(aliases=None):
    """Fail if any migrations are pending"""
    for db_conn in connections.all():
        if aliases and db_conn.alias not in aliases:
            continue
        executor = MigrationExecutor(db_conn)
        plan = executor.migration_plan(executor.loader.graph.leaf_nodes())
        if plan:
            log.error("Migrations pending on '%s' database", db_conn.alias)
            raise HealthcheckFailure("database migrations pending")
