from django.shortcuts import redirect
from django.urls import reverse
import jwt
from django.conf import settings

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/users/profile':
            jwt_token = request.COOKIES.get('jwt_token')
            if not jwt_token:
                return redirect(reverse('users:login')) 
            try:
                jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                return redirect(reverse('users:login'))
            except jwt.InvalidTokenError:
                return redirect(reverse('users:login'))
        response = self.get_response(request)
        return response
