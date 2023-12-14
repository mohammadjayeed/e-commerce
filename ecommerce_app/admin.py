from django.contrib import admin
from .models import Customer, Product, Review, Cart
# Register your models here.
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Review)
admin.site.register(Cart)