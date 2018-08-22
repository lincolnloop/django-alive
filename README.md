# django-alive 🕺

[![tests](https://img.shields.io/travis/lincolnloop/django-alive/master.svg)](https://travis-ci.org/lincolnloop/django-alive)
[![coverage](https://img.shields.io/codacy/coverage/5d539d4956a44f55aec632f3a43ee6c1/master.svg)](https://app.codacy.com/project/ipmb/django-alive/dashboard)
[![PyPI](https://img.shields.io/pypi/v/django-alive.svg)](https://pypi.org/project/django-alive/)
![Python Versions](https://img.shields.io/pypi/pyversions/django-alive.svg)

Provides two healthcheck endpoints for your Django application:

**Alive**

Verifies the WSGI server is responding.

* Default URL: `/-/alive/`
* Success:
    * status code: `200`
    * content: `ok`
* Failure: This view never returns a failure. A failure would mean your WSGI server is not running.

**Health**

Verifies services are ready.

* Default URL: `/-/health/`
* Success:
    * status_code: `200`
    * content: `{"healthy": true}`
* Failure:
    * status_code: `503`
    * content: `{"healthy": false, "errors": ["error 1", "error 2"]}`

By default the health endpoint will test the database connection, but can be configured to check the cache, staticfiles, or any additional custom checks.

Supports Django 1.10+ on both Python 2 & 3.

## Install

```
pip install django-alive
```

## Configure

Add this to your project's `urlpatterns`:

```python
path("-/", include("django_alive.urls"))
```

For versions before Django 2.0, use:

```python
url(r"-/", include("django_alive.urls"))
```

## Enabling Checks

The default "health" endpoint will test a simple `SELECT 1` query on the database. Additional checks can be enabled in your Django settings.

Use the `ALIVE_CHECKS` setting to configure the checks to include. It is a dictionary with the path to a Python function as a key and any keyword arguments to pass to that function as a value. A full example:

```python
ALIVE_CHECKS = {
    "django_alive.checks.check_database": {},
    "django_alive.checks.check_staticfiles": {
        "filename": "img/favicon.ico",
    },
    "django_alive.checks.check_cache": {
        "cache": "session",
        "key": "test123",
    },
}

```

## Custom Checks

`django-alive` is designed to easily extend with your own custom checks. Simply define a function which performs your check and raises a `django_alive.HealthcheckFailure` exception in the event of a failure. See [`checks.py`](https://github.com/lincolnloop/django-alive/blob/master/django_alive/checks.py) for some examples on how to write a check.

## Bypassing the `ALLOWED_HOSTS` Check

Often, load balancers will not pass a `Host` header when probing a healthcheck endpoint. This presents a problem for [Django's host header validation](https://docs.djangoproject.com/en/2.1/topics/security/#host-headers-virtual-hosting). A middleware is included that will turn off the host checking only for the healthcheck endpoints. This is safe since these views never do anything with the `Host` header.

Enable the middleware by inserting this **at the beginning** of your `MIDDLEWARES`:

```python
MIDDLEWARES = [
    "django_alive.middleware.healthcheck_bypass_host_check",
    # ...
]
```
