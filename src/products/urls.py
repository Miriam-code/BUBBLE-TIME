from django.urls import path
from products.views import index
from products.views import order_history

app_name = "products"
urlpatterns = [
  path('', index, name='index'),
  path('order_history/', order_history, name='order_history'),
]
