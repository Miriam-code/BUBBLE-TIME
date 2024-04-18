from django.shortcuts import render
from .forms import CommandeForm
from .models import OrdersItem

def index(request):
    if request.method == 'POST':
        form = CommandeForm(request.POST)
        if form.is_valid():
        # django nettoye, valide et enregistre => dictionnaire
            basic_taste = form.cleaned_data['basic_taste']
            topping = form.cleaned_data['topping']
            sugar = form.cleaned_data['sugar']
            size = form.cleaned_data['size']
            quantity = form.cleaned_data['quantity']
            
            order_item = OrdersItem(
                basic_taste=basic_taste,
                topping=topping,
                sugar=sugar,
                size=size,
                quantity=quantity
            )
            order_item.save()
            
            return render(request, 'products/index.html')
    else:
        form = CommandeForm()
    
    return render(request, 'products/index.html', {'form': form})

def order_history(request):
    orders = OrdersItem.objects.all()
    return render(request, 'products/order_history.html', {'orders': orders})
