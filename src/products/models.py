from django.db import models

class OrdersItem(models.Model):
    basic_taste = models.CharField(max_length=100)
    topping = models.CharField(max_length=100)
    sugar = models.IntegerField()
    size = models.CharField(max_length=10)
    quantity = models.IntegerField()
    
    class Meta:
        db_table = 'orders_items'