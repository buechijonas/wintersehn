from rest_framework.exceptions import Throttled
from rest_framework.throttling import SimpleRateThrottle


def client_ip(request):
    return request.META.get("HTTP_X_REAL_IP") or request.META.get("REMOTE_ADDR")


class LoginThrottled(Throttled):
    default_detail = "Zu viele Anmeldeversuche."
    extra_detail_singular = "Bitte versuche es in {wait} Sekunde erneut."
    extra_detail_plural = "Bitte versuche es in {wait} Sekunden erneut."


class LoginIpRateThrottle(SimpleRateThrottle):
    scope = "login_ip"

    def get_cache_key(self, request, view):
        return self.cache_format % {"scope": self.scope, "ident": client_ip(request)}


class LoginUsernameRateThrottle(SimpleRateThrottle):
    # Limits attempts against a single account, even when they're spread
    # over many IP addresses.
    scope = "login_username"

    def get_cache_key(self, request, view):
        username = str(request.data.get("username") or "").strip().lower()
        if not username:
            return None
        return self.cache_format % {"scope": self.scope, "ident": username}
