from django.contrib import admin
from .models import Customer, Product, Review, Cart, Order, OrderItem
# Register your models here.
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Review)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)