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
        form = OrdersItemForm()
    return render(request, 'commande.html', {'form': form})

def liste_commandes(request):
    commandes = OrdersItem.objects.all()
    return render(request, 'liste_commandes.html', {'commandes': commandes})