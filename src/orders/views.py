from django.shortcuts import render


def history(request):
  return render(request, 'orders/history.html')

def basket(request):
  return render(request, 'orders/basket.html')
