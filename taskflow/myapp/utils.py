from django.core.cache import cache
from django.http import JsonResponse
from rest_framework import status
from functools import wraps
from django.conf import settings
import time


def rate_limit(requests=5, interval=60):
    """
    Rate limiting decorator that limits the number of requests within a specific timeframe.
    :param requests: Number of allowed requests within the interval
    :param interval: Time interval in seconds
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(view_instance, request, *args, **kwargs):
            # Get client IP address
            client_ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
            
            # Create a unique cache key for this client and endpoint
            cache_key = f"rate_limit_{client_ip}_{request.path}"
            
            # Get the list of request timestamps for this client and endpoint
            requests_timestamps = cache.get(cache_key, [])
            now = time.time()

            # Remove timestamps older than the interval
            requests_timestamps = [ts for ts in requests_timestamps if now - ts < interval]

            # If number of requests exceeds limit, return 429 Too Many Requests
            if len(requests_timestamps) >= requests:
                remaining_time = int(interval - (now - requests_timestamps[0]))
                headers = {
                    'X-RateLimit-Limit': str(requests),
                    'X-RateLimit-Remaining': '0',
                    'Retry-After': str(remaining_time)
                }
                return JsonResponse(
                    {
                        'error': 'Too many requests. Please try again later.',
                        'retry_after_seconds': remaining_time
                    },
                    status=status.HTTP_429_TOO_MANY_REQUESTS,
                    headers=headers
                )

            # Add current timestamp to list and update cache
            requests_timestamps.append(now)
            cache.set(cache_key, requests_timestamps, interval)

            # Add rate limit headers to response
            response = view_func(view_instance, request, *args, **kwargs)
            response['X-RateLimit-Limit'] = str(requests)
            response['X-RateLimit-Remaining'] = str(requests - len(requests_timestamps))

            return response
        return _wrapped_view
    return decorator
