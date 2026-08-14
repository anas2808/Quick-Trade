from django.conf import settings
from django.shortcuts import redirect


class CanonicalHostMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        canonical_host = getattr(settings, 'APP_CANONICAL_HOST', None)
        canonical_scheme = getattr(settings, 'APP_CANONICAL_SCHEME', 'https')
        if not settings.DEBUG and canonical_host:
            current_host = request.get_host().split(':', 1)[0]
            if current_host != canonical_host:
                target_url = f'{canonical_scheme}://{canonical_host}{request.get_full_path()}'
                return redirect(target_url, permanent=True)
        return self.get_response(request)
