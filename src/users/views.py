from django.shortcuts import render, redirect
from django.db import connection
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from datetime import timedelta

def sign_up(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM users WHERE email = %s", [email])
            user_count = cursor.fetchone()[0]

        if user_count > 0:
            return render(request, 'users/register.html', {'error': 'Cet email est déjà utilisé.'})

        hashed_password = make_password(password)
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)",
                           [first_name, last_name, email, hashed_password])

        return redirect('users:login')

    else:
        return render(request, 'users/register.html')

def sign_in(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        with connection.cursor() as cursor:
            cursor.execute("SELECT id, email, password FROM users WHERE email = %s", [email])
            user_data = cursor.fetchone()

        if user_data is not None:
            user_id, db_email, db_password = user_data

            if check_password(password, db_password):
                expiry_time = timezone.now() + timedelta(hours=4)

                return redirect('users:profile')

        # Si les informations d'identification sont incorrectes, afficher un message d'erreur
        return render(request, 'users/login.html', {'error': 'Email ou mot de passe incorrect.'})

    else:
        return render(request, 'users/login.html')

def get_me(request):
  return render(request, 'users/profile.html')
