from django import forms
from .models import OrdersItem

class OrdersItemForm(forms.ModelForm):
    class Meta:
        model = OrdersItem
        fields = ['basic_taste', 'topping', 'sugar', 'size', 'price', 'quantity', 'orders_id']
