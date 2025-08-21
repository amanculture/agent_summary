

from django.http import JsonResponse
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timedelta
from decouple import config
import logging


# -------------------- RestrictDomainMiddleware --------------------

class RestrictDomainMiddleware:
    TRUSTED_DOMAINS = [
        'http://localhost:5173',   # React Localhost (Dev)
        'http://localhost:5174',   # Optional Dev port
        'http://127.0.0.1:8000',   # Django Localhost
        'http://localhost:8000',
        'https://insights.cultureholidays.com',
        
        
    ]

    EXCLUDED_PATHS = [
        '/admin/login/',
        '/inactive-agent',
        '/agentdata',
        '/trav-info',
        '/code-terminal',
        '/admin',
        '/guess-gender',
    ]

    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger('middleware')
        self.dynamic_domains = self.TRUSTED_DOMAINS.copy()
        self.last_origin_root = None  # Stores last known "base" origin


    def __call__(self, request):
        path = request.path
        origin = request.META.get('HTTP_ORIGIN') or request.META.get('HTTP_REFERER')
        client_ip = request.META.get('REMOTE_ADDR')

        # dynamic_domains = self.TRUSTED_DOMAINS.copy()

        
        # print("Origin : ", origin)
        # print('Dynamic Domain 1 :', self.dynamic_domains)

        self.logger.debug("Origin: %s", origin)
        self.logger.debug("Dynamic Domains (Before): %s", self.dynamic_domains)

        # 👇 If initial request comes from trusted localhost, allow tunnel too
        if origin and (
            origin.startswith('https://insights.cultureholidays.com') or 
            origin.startswith('https://reports.cultureholidays.com/plotly/report') or 
            origin.startswith('https://reports.cultureholidays.com/django_plotly_dash/app/DataTableApp')
        ):
            if 'https://reports.cultureholidays.com' not in self.dynamic_domains:
                # print("Adding dynamic domain for reports")
                self.logger.debug("Adding dynamic domain for reports")
                self.dynamic_domains.append('https://reports.cultureholidays.com')


        # print("-----------------------------------------------")
        # print("-----------------------------------------------")
        # print('Dynamic Domain 2 :', self.dynamic_domains)
        # print("=== Middleware Debug ===")
        # print("Request path:", path)
        # print("Origin / Referer header:", origin)
        # print("Client IP:", client_ip)

        self.logger.debug("-----------------------------------------------")
        self.logger.debug("-----------------------------------------------")
        self.logger.debug("Dynamic Domains (After): %s", self.dynamic_domains)
        self.logger.debug("=== Middleware Debug ===")
        self.logger.debug("Request path: %s", path)
        self.logger.debug("Origin / Referer header: %s", origin)
        self.logger.debug("Client IP: %s", client_ip)



        if (
            path.startswith('/api/')
            or path.startswith('/plotly/')
            or path.startswith('/django_plotly_dash/')
        ) and not any(path.startswith(excluded) for excluded in self.EXCLUDED_PATHS):

            # 🧠 Handle requests with origin
            if origin:
                origin_base = origin.lower().split('?')[0]
                if not any(origin_base.startswith(domain.lower()) for domain in self.dynamic_domains):
                    # print("⛔ Blocked - Origin not trusted:", origin_base)
                    self.logger.warning("Blocked - Origin not trusted: %s", origin_base)
                    return JsonResponse({'error': 'Access denied: Unauthorized domain'}, status=403)

            # 🔄 Handle Dash internal calls without origin
            else:
                if path.startswith('/django_plotly_dash/'):
                    self.logger.debug("✅ Allowed internal Dash call with no origin") 
                    # print("✅ Allowed internal Dash call with no origin")
                    return self.get_response(request)

                # 🚫 No origin and not internal Dash → deny unless localhost
                if client_ip not in ('127.0.0.1', '::1'):
                    # print("⛔ Blocked - No origin and not localhost")
                    self.logger.warning("Blocked - No origin and not localhost")
                    return JsonResponse({'error': 'Access denied: No origin provided'}, status=403)

        return self.get_response(request)



# -------------------- JWTAuthenticationMiddleware --------------------

JWT_SECRET = config('SECRET_KEY')
JWT_ALGORITHM = config('JWT_ALGORITHM')

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_paths = [
            '/login',
            '/agentdata',
            '/inactive-agent',
            '/admin/login/',
            '/plotly/',
            '/django_plotly_dash/',
            '/trav-info',
            '/code-terminal',
            '/admin',
            '/guess-gender',
        ]

    def __call__(self, request):
        path = request.path

        # Skip JWT for exempted paths
        if any(path.startswith(p) for p in self.exempt_paths):
            return self.get_response(request)

        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return JsonResponse({'success': False, 'message': 'Authorization header missing or malformed'}, status=401)

        token = auth_header.replace('Bearer ', '', 1).strip()
        if not token:
            return JsonResponse({'success': False, 'message': 'Token missing'}, status=401)

        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            request.user = payload.get('username')

            exp_timestamp = payload.get('exp')
            if exp_timestamp:
                expiry_time_utc = datetime.utcfromtimestamp(exp_timestamp)
                expiry_time_ist = expiry_time_utc + timedelta(hours=5, minutes=30)
                # print(f"[Middleware] Token expiry (IST): {expiry_time_ist}")

        except ExpiredSignatureError:
            return JsonResponse({'success': False, 'message': 'Token has expired'}, status=401)
        except InvalidTokenError:
            return JsonResponse({'success': False, 'message': 'Invalid token'}, status=401)

        return self.get_response(request)
