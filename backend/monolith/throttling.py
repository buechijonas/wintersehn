from rest_framework.throttling import SimpleRateThrottle


class ShareLinkIPThrottle(SimpleRateThrottle):
    scope = "share_link_ip"

    def get_cache_key(self, request, view):
        ident = request.META.get("HTTP_X_REAL_IP") or self.get_ident(request)
        return self.cache_format % {"scope": self.scope, "ident": ident}


class ShareLinkThrottle(SimpleRateThrottle):
    scope = "share_link"

    def get_cache_key(self, request, view):
        return self.cache_format % {"scope": self.scope, "ident": view.kwargs["token"]}
