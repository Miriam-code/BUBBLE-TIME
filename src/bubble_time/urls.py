
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls')),
    path('app/', include('users.urls')),
    path('app/orders/', include('orders.urls')),
]
