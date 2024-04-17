from django import forms
from .models import OrdersItem

class CommandeForm(forms.ModelForm):
    class Meta:
        model = OrdersItem
        fields = ['basic_taste', 'topping', 'sugar', 'size', 'quantity']