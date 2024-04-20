from django.shortcuts import render, redirect
from django.db import connection
from django.contrib.auth.hashers import make_password, check_password
from users.forms import RegisterForm
import jwt
from datetime import datetime, timedelta
from .utils import verify_token
from django.http import HttpResponse
from django.contrib.auth import logout
from django.http import Http404


def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM users WHERE email = %s", [email])
                user_count = cursor.fetchone()[0]

            if user_count > 0:
                form.add_error('email', 'Cet email est déjà utilisé.')
                return render(request, 'users/register.html', {'form': form})

            hashed_password = make_password(password)
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)",
                               [first_name, last_name, email, hashed_password])

                user_id = cursor.lastrowid

            payload = {
                'user_id': user_id,
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'exp': datetime.utcnow() + timedelta(days=1) 
            }
            token = jwt.encode(payload, 'django-insecure-^lgnf#+i0&!-=$3utocui=@iy)8toj!-0+dc!p4mark%ttl+wy', algorithm='HS256')

            response = redirect('users:profile')
            response.set_cookie('jwt_token', token)

            return response

    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})

def sign_in(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        with connection.cursor() as cursor:
            cursor.execute("SELECT id, first_name, last_name, email, password FROM users WHERE email = %s", [email])
            user_data = cursor.fetchone()

        if user_data is not None:
            user_id, first_name, last_name, db_email, db_password = user_data

            if check_password(password, db_password):
                payload = {
                    'user_id': user_id,
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'exp': datetime.utcnow() + timedelta(days=1)
                }
                token = jwt.encode(payload, 'django-insecure-^lgnf#+i0&!-=$3utocui=@iy)8toj!-0+dc!p4mark%ttl+wy', algorithm='HS256')

                response = redirect('users:profile')
                response.set_cookie('jwt_token', token)

                return response
            else:
                return render(request, 'users/login.html', {'error': 'Mot de passe incorrect.'})
        else:
            return render(request, 'users/login.html', {'error': 'Email incorrect.'})

    else:
        return render(request, 'users/login.html')

def get_user_orders(user_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM orders WHERE user_id = %s", [user_id])
        user_orders = cursor.fetchall()

        orders_detail = []
        for order in user_orders:
            
            cursor.execute("SELECT * FROM orders_items WHERE orders_id = %s", [order[0]])
            items = cursor.fetchall()

            print('items', items)

            order_detail = {
                'order': order,
                'items': items
            }
            orders_detail.append(order_detail)

    return orders_detail

def get_me(request):
    payload = verify_token(request)
    is_authenticated = False

    if payload:
        user_email = payload.get('email')

        with connection.cursor() as cursor:
            cursor.execute("SELECT id, first_name, last_name, email FROM users WHERE email = %s", [user_email])
            user_data = cursor.fetchone()

        if user_data:
            user_id, first_name, last_name, email = user_data
            is_authenticated = True
            
            orders_detail = get_user_orders(user_id)

            print('orders details' , orders_detail)
            
            return render(request, 'users/profile.html', {
                'user': {'id': user_id, 'first_name': first_name, 'last_name': last_name, 'email': email}, 
                'is_authenticated': is_authenticated,
                'orders_detail': orders_detail 
            })
        else:
            return HttpResponse("Utilisateur non trouvé.")
    else:
        return HttpResponse("Token non trouvé. Veuillez vous connecter.")

    
def logout(request):
    response = redirect('products:index')
    response.delete_cookie('jwt_token')
    return response
    
def auth_context(request):
    payload = verify_token(request)
    is_authenticated = False
    user_data = None

    if payload:
        is_authenticated = True
        user_data = {
            'user_id': payload.get('user_id'),
            'first_name': payload.get('first_name'),
            'last_name': payload.get('last_name'),
            'email': payload.get('email')
        }

    return {'is_authenticated': is_authenticated, 'user_data': user_data}

def update_profile(request):
    auth_data = auth_context(request)
    
    if auth_data['is_authenticated']:
        user_id = auth_data['user_data']['user_id']
        
        if request.method == 'POST':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            password = request.POST.get('password')

            if first_name and last_name and password:
                hashed_password = make_password(password)

                with connection.cursor() as cursor:
                    try:
                        print("User id:", user_id)
                        cursor.execute("UPDATE users SET first_name = %s, last_name = %s, password = %s WHERE id = %s", [first_name, last_name, hashed_password, user_id])
                        print("Profil utilisateur mis à jour avec succès.")
                    except Exception as e:
                        print("Erreur lors de la mise à jour du profil utilisateur:", e)

                auth_data['user_data']['first_name'] = first_name
                auth_data['user_data']['last_name'] = last_name
                return render(request, 'users/profile.html', {'user': auth_data['user_data']})
            else:
                print("Données manquantes pour la mise à jour du profil.")
        else:
            print("Méthode HTTP non autorisée pour cette vue.")
    else:
        print("Utilisateur non authentifié.")

    return render(request, 'users/profile.html')



def delete_profile(request):
    auth_data = auth_context(request)
    
    if auth_data['is_authenticated']:
        user_id = auth_data['user_data']['user_id']
        print('user_id',user_id)
        
        if request.method == 'POST':
            with connection.cursor() as cursor:
                try:
                    cursor.execute("DELETE FROM users WHERE id = %s", [user_id])
                    print("Utilisateur supprimé avec succès")
                    return logout(request)
                except Exception as e:
                    print("Erreur lors de la suppression de l'utilisateur:", e)
        else:
            print("Méthode HTTP non autorisée")
    else:
        print("Utilisateur non authentifié")

    return render(request, 'users/profile.html')