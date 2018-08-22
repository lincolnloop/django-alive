from django.core.exceptions import DisallowedHost
from django.urls import reverse
from django.test import TestCase, RequestFactory, override_settings

from ..middleware import healthcheck_bypass_host_check

class MiddlewareTestCase(TestCase):
    def setUp(self):
        self.middleware = healthcheck_bypass_host_check(lambda r: r)

    @override_settings(ALLOWED_HOSTS=["not-testserver"])
    def test_bypass(self):
        request = RequestFactory().get(reverse("alive_alive"))
        passed_request = self.middleware(request)
        self.assertEqual(request, passed_request)

    @override_settings(ALLOWED_HOSTS=["not-testserver"])
    def test_disallowed(self):
        request = RequestFactory().get("/")
        request = self.middleware(request)
        self.assertRaises(DisallowedHost, request.get_host)



