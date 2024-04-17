from django.urls import path
from orders.views import history, basket

urlpatterns = [
  path('history', history, name='history'),
  path('basket', basket, name='basket'),

]