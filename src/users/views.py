from django.shortcuts import render, redirect
from django.db import connection
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError
from users.forms import RegisterForm


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

            # Redirection vers le profil de l'utilisateur après l'inscription
            return redirect('users:profile')

    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})

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

        return render(request, 'users/login.html', {'error': 'Email ou mot de passe incorrect.'})

    else:
        return render(request, 'users/login.html')

def get_me(request):
  return render(request, 'users/profile.html')
