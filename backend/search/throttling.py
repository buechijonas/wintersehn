from rest_framework.throttling import SimpleRateThrottle


class HostRatingsThrottle(SimpleRateThrottle):
    scope = "host_ratings"

    def get_cache_key(self, request, view):
        ident = request.META.get("HTTP_X_REAL_IP") or self.get_ident(request)
        return self.cache_format % {"scope": self.scope, "ident": ident}
