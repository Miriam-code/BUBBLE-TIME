from django.urls import path
from orders.views import history, basket, ajouter_panier, valider_panier, vider_panier

app_name = 'orders'


urlpatterns = [
  path('history', history, name='history'),
  path('basket', basket, name='basket'),
  path('ajouter_panier/', ajouter_panier, name='ajouter_panier'),
  path('valider_panier/', valider_panier, name='valider_panier'),
  path('vider_panier/', vider_panier, name='vider_panier')
]