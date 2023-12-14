from django.contrib import admin
from .models import Customer, Product, Review
# Register your models here.
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Review)