from django.http import HttpResponseForbidden
from django.core.cache import cache
from django.conf import settings
import time

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.path.startswith('/admin/'):
            ip = self.get_client_ip(request)
            key = f'rate_limit_{ip}'
            
            requests = cache.get(key, {'count': 0, 'timestamp': time.time()})

            if time.time() - requests['timestamp'] > settings.RATE_LIMIT_WINDOW:
                requests = {'count': 0, 'timestamp': time.time()}
            
            requests['count'] += 1
            cache.set(key, requests, settings.RATE_LIMIT_WINDOW)
            
            if requests['count'] > settings.RATE_LIMIT_REQUESTS:
                response = HttpResponseForbidden("Rate limit exceeded. Please try again later.")
                response['X-RateLimit-Limit'] = str(settings.RATE_LIMIT_REQUESTS)
                response['X-RateLimit-Remaining'] = '0'
                response['X-RateLimit-Reset'] = str(int(requests['timestamp'] + settings.RATE_LIMIT_WINDOW))
                return response

            response = self.get_response(request)
            response['X-RateLimit-Limit'] = str(settings.RATE_LIMIT_REQUESTS)
            response['X-RateLimit-Remaining'] = str(settings.RATE_LIMIT_REQUESTS - requests['count'])
            response['X-RateLimit-Reset'] = str(int(requests['timestamp'] + settings.RATE_LIMIT_WINDOW))
            return response

        return self.get_response(request)

    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
