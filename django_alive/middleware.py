from django.urls import reverse


def healthcheck_bypass_host_check(get_response):
    healthcheck_urls = [reverse("alive_alive"), reverse("alive_health")]

    def middleware(request):
        if request.path in healthcheck_urls:
            request.get_host = request._get_raw_host

        return get_response(request)

    return middleware
