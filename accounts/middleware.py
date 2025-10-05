from .models import AuditLog

class AuditLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        try:
            AuditLog.objects.create(
                user=request.user if getattr(request, 'user', None) and request.user.is_authenticated else None,
                path=request.path,
                method=request.method,
                ip=request.META.get('REMOTE_ADDR', ''),
                status_code=response.status_code,
            )
        except Exception:
            # Avoid breaking requests due to audit log failures
            pass
        return response
