# middleware.py
from django.shortcuts import render
from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseForbidden
import re

class UniversalRateLimitMiddleware(MiddlewareMixin):
    """
    Universal Rate Limit Middleware - Limits requests per IP across entire website
    """
    
    # Configuration
    RATE_LIMIT = 100  # Maximum requests per time window
    TIME_WINDOW = 60  # Time window in seconds (60 seconds = 1 minute)
    BLOCK_DURATION = 60  # Block duration in seconds (300 seconds = 5 minutes)
    
    # URLs to exclude from rate limiting (whitelist)
    EXCLUDED_URLS = [
        r'^/admin/',           # Admin panel
        r'^/static/',          # Static files
        r'^/media/',           # Media files
        r'^/favicon\.ico$',    # Favicon
        r'^/robots\.txt$',     # Robots.txt
    ]
    
    # APIs/AJAX endpoints that need higher limits
    HIGHER_LIMIT_URLS = {
        r'^/api/': 500,        # API endpoints: 500 requests per minute
        r'^/contact/': 20,     # Contact page: 20 requests per minute
        r'^/about-us/': 10,     # Contact page: 20 requests per minute
        r'^/': 10,     # Contact page: 20 requests per minute
        r'^/blog/': 10,     # Contact page: 20 requests per minute
        r'^/courses/': 10,     # Contact page: 20 requests per minute
        r'^/schedule/': 10,     # Contact page: 20 requests per minute
    }
    
    def get_client_ip(self, request):
        """Get real client IP address even behind proxy"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        
        # Handle localhost
        if ip == '127.0.0.1' or ip == '::1':
            return ip
        
        return ip
    
    def is_excluded_url(self, path):
        """Check if URL should be excluded from rate limiting"""
        for pattern in self.EXCLUDED_URLS:
            if re.match(pattern, path):
                return True
        return False
    
    def get_rate_limit_for_url(self, path):
        """Get specific rate limit for URL if configured"""
        for pattern, limit in self.HIGHER_LIMIT_URLS.items():
            if re.match(pattern, path):
                return limit
        return self.RATE_LIMIT
    
    def process_request(self, request):
        """Process each request and apply rate limiting"""
        
        # Skip rate limiting for excluded URLs
        if self.is_excluded_url(request.path):
            return None
        
        # Get client IP
        client_ip = self.get_client_ip(request)
        
        # Skip rate limiting for localhost (optional - remove in production)
        # if client_ip in ['127.0.0.1', '::1']:
        #     return None
        
        # Check if IP is currently blocked
        block_key = f'rate_limit_blocked_{client_ip}'
        if cache.get(block_key):
            # IP is blocked - show custom page
            return render(request, 'home/rate_limit_exceeded.html', 
                         {'block_duration': self.BLOCK_DURATION // 60},
                         status=429)
        
        # Get rate limit for this URL
        rate_limit = self.get_rate_limit_for_url(request.path)
        
        # Rate limit key based on IP and minute window
        current_minute = int(cache.get('rate_limit_timestamp', 0))
        if not current_minute:
            current_minute = int(__import__('time').time() // self.TIME_WINDOW)
            cache.set('rate_limit_timestamp', current_minute, self.TIME_WINDOW + 10)
        
        key = f'rate_limit_{client_ip}_{current_minute}'
        
        # Get current request count
        request_count = cache.get(key, 0)
        
        if request_count >= rate_limit:
            # Rate limit exceeded - block this IP
            cache.set(block_key, True, self.BLOCK_DURATION)
            return render(request, 'home/rate_limit_exceeded.html', 
                         {'block_duration': self.BLOCK_DURATION // 60},
                         status=429)
        
        # Increment request count
        cache.set(key, request_count + 1, self.TIME_WINDOW + 10)
        
        # Add rate limit headers for transparency
        request.META['X-RateLimit-Limit'] = str(rate_limit)
        request.META['X-RateLimit-Remaining'] = str(rate_limit - request_count - 1)
        
        return None
    
    def process_response(self, request, response):
        """Add rate limit headers to response"""
        if hasattr(request, 'META'):
            if 'X-RateLimit-Limit' in request.META:
                response['X-RateLimit-Limit'] = request.META['X-RateLimit-Limit']
            if 'X-RateLimit-Remaining' in request.META:
                response['X-RateLimit-Remaining'] = request.META['X-RateLimit-Remaining']
        
        # Add retry-after header if rate limited
        if response.status_code == 429:
            response['Retry-After'] = str(self.BLOCK_DURATION)
        
        return response