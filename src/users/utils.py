import jwt

def verify_token(request):
    jwt_token = request.COOKIES.get('jwt_token')

    if jwt_token:
        try:
            payload = jwt.decode(jwt_token, 'django-insecure-^lgnf#+i0&!-=$3utocui=@iy)8toj!-0+dc!p4mark%ttl+wy', algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    return None
