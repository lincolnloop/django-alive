import os

try:
    from django.urls import include, re_path
except:
    from django.conf.urls import include, url as re_path

CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
ROOT_URLCONF = "django_alive.tests.settings"
SECRET_KEY = "secret"

STATIC_ROOT = os.path.join(os.path.dirname(__file__), "static")
STATIC_URL = "/static/"


urlpatterns = [re_path(r"-/", include("django_alive.urls"))]
