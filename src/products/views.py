from django.shortcuts import render
from django.db import connection

def index(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT basic_taste , toppings FROM bubbles")
        bubbles = cursor.fetchall()
        images = ['milk.png','chocolate.png','coffee.png','pineapple.png','strawberry.png','peach.png']
    return render(request, 'products/index.html', {'bubbles': bubbles , 'images':images})
