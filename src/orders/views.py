from django.shortcuts import render, redirect
from django.db import connection
from users.utils import verify_token
from users.views import auth_context

panier = []

def vider_panier(request):
    panier.clear()
    return redirect('orders:basket')

def history(request):
  return render(request, 'orders/history.html')

def ajouter_panier(request):
    global panier_items
    
    if request.method == 'POST':
        basic_taste = request.POST.get('basic_taste')
        topping = request.POST.get('topping')
        sugar = request.POST.get('sugar')
        size = request.POST.get('size')
        quantity = int(request.POST.get('quantity'))


        if size == 'small':
            prix_unitaire = 4.00
        elif size == 'medium':
            prix_unitaire = 5.50
        else:
            prix_unitaire = 6.50


        total = prix_unitaire * quantity

        item = {
            'basic_taste': basic_taste,
            'topping': topping,
            'sugar': sugar,
            'size': size,
            'quantity': quantity,
            'unit_price': prix_unitaire,
            'total': total
        }

        panier.append(item)

        return redirect('orders:basket')
    else:
        return redirect('index')

def basket(request):
    total_global = sum(item['total'] for item in panier)
    return render(request, 'orders/basket.html', {'panier': panier, 'total_global': total_global})

def valider_panier(request):

    if request.method == 'POST':
        auth_context_data = auth_context(request)  
        if auth_context_data['is_authenticated']:
            user_id = auth_context_data['user_data']['user_id'] 
        
            total_global = sum(item['total'] for item in panier)
            
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO orders (total, status, user_id) VALUES (%s, 'en cours de préparation', %s)", [total_global, user_id])
                order_id = cursor.lastrowid 
            
            for item in panier:
                basic_taste = item['basic_taste']
                topping = item['topping']
                sugar = item['sugar']
                size = item['size']
                price = item['total']
                quantity = item['quantity']
                
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO orders_items (basic_taste, topping, sugar, size, price, quantity, orders_id) VALUES (%s, %s, %s, %s, %s, %s, %s)", [basic_taste, topping, sugar, size, price, quantity, order_id])

            return redirect('users:profile')
        else:
            return redirect('users:login')
    else:
        return redirect('index')
