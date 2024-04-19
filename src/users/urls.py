from django.urls import path
from users.views import sign_up, sign_in, get_me, logout, update_profile, delete_profile

app_name = "users"
urlpatterns = [
    path('register', sign_up, name='register'),
    path('login', sign_in, name='login'),
    path('profile/', get_me, name='profile'),
    path('logout', logout, name='logout'),
    path('profile/update_profile', update_profile, name='update_profile'),
    path('profile/delete_profile', delete_profile, name='delete_profile'),
]