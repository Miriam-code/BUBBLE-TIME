from django.shortcuts import render

def sign_up(request):
  return render(request, 'users/register.html')

def sign_in(request):
  return render(request, 'users/login.html')

def get_me(request):
  return render(request, 'users/profile.html')
