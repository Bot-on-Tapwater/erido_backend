# your_app/middleware.py
from django.utils.deprecation import MiddlewareMixin
from django.views.decorators.csrf import ensure_csrf_cookie

class EnsureCSRFMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        return ensure_csrf_cookie(view_func)(request, *view_args, **view_kwargs)
