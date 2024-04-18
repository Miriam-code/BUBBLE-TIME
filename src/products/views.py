from django.shortcuts import render, redirect
from django.forms import Form
from .forms import OrdersItemForm
from .models import OrdersItem

def passer_commande(request):
    if request.method == 'POST':
        form = OrdersItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_commandes')
    else:
        form = CommandeForm()
    
    return render(request, 'products/index.html', {'form': form})

def order_history(request):
    orders = OrdersItem.objects.all()
    return render(request, 'products/order_history.html', {'orders': orders})
