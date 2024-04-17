# Create your models here.

# class Departments(models.Model):
#     DepartmentId = models.AutoField(primary_key=True)
#     DepartementName = models.CharField(max_length=500)

# class Employees(models.Model):
#     EmployeeId = models.AutoField(primary_key=True)
#     EmployeeName = models.CharField(max_length=500)
#     Departement = models.CharField(max_length=500)
#     DateOfJoining = models.DataField()
#     PhotoFileName = models.CharField(max_length=500)

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class OrdersItem(models.Model):
    BASIC_TASTE_CHOICES = [
        ('milk_coffee', 'Milk Coffee'),
        ('milk_chocolate', 'Milk Chocolate'),
        ('milk_vanilla', 'Milk Vanilla'),
        ('fruit', 'Fruit'),
    ]
    TOPPING_CHOICES = [
        ('tapioca', 'Tapioca'),
        ('strawberry', 'Strawberry'),
        ('pineapple', 'Pineapple'),
        ('peach', 'Peach'),
        ('kiwi', 'Kiwi'),
        ('cherry', 'Cherry'),
        ('apple', 'Apple'),
    ]
    SIZE_CHOICES = [
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('large', 'Large'),
    ]
    
    basic_taste = models.CharField(max_length=20, choices=BASIC_TASTE_CHOICES)
    topping = models.CharField(max_length=20, choices=TOPPING_CHOICES)
    sugar = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    size = models.CharField(max_length=10, choices=SIZE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    orders_id = models.IntegerField()

    def __str__(self):
        return f"Order Item {self.id}"

