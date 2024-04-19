from django.db import models

class Bubble(models.Model):
    basic_taste = models.CharField(max_length=50, null=True)
    toppings = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f"Basic Taste: {self.basic_taste}, Toppings: {self.toppings}"
    
    class Meta:
        db_table = 'bubbles'
