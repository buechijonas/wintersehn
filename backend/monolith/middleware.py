from .models import AccessLog

API_PREFIX = "/api/monolith/"


class AuditMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if not request.path.startswith(API_PREFIX):
            return response
        AccessLog.objects.create(
            user=request.user if request.user.is_authenticated else None,
            method=request.method,
            path=request.path[:500],
            status=response.status_code,
        )
        response.setdefault("Cache-Control", "no-store")
        return response
