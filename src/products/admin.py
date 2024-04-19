from django.contrib import admin
from .models import Bubble

class BubbleAdmin(admin.ModelAdmin):
    list_display = ('basic_taste', 'toppings')
    search_fields = ('basic_taste', 'toppings')

admin.site.register(Bubble, BubbleAdmin)
