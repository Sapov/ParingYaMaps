from django.contrib import admin

from .models import Links, Order, Category, City, OrderStatus


admin.site.register(Links)
admin.site.register(Order)
admin.site.register(Category)
admin.site.register(City)
admin.site.register(OrderStatus)