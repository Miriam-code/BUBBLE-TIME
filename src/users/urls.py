from django.urls import path
from users.views import sign_up, sign_in,get_me

app_name = "users"
urlpatterns = [
  path('register', sign_up, name='register'),
  path('login', sign_in, name='login'),
  path('profile', get_me, name='profile'),
]