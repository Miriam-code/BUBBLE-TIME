from django.shortcuts import redirect
from django.urls import reverse
import jwt
from django.conf import settings

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        jwt_token = request.COOKIES.get('jwt_token')

        if request.path == '/users/profile':
            if not jwt_token:
                return redirect(reverse('users:login')) 

            try:
                jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                return redirect(reverse('users:login'))
            except jwt.InvalidTokenError:
                return redirect(reverse('users:login'))

        elif request.path in ['/users/login', '/users/register']:
            if jwt_token:
                return redirect(reverse('products:index'))

        response = self.get_response(request)
        return response
