from django.core.validators import MinValueValidator
from django.db import models
from uuid import uuid4
from django.contrib.auth.models import User
from django.utils.text import slugify

class Product(models.Model):
    title = models.CharField(max_length=255)
    slug= models.SlugField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    unit_price = models.DecimalField(max_digits=6,decimal_places=2,validators=[MinValueValidator(1)])
    last_update = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
class Customer(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=255,null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    

    def __str__(self):
        return f'Customer {self.id}'

class Order(models.Model):
    

    placed_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='orderitems')
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)




class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        unique_together = ('cart', 'product')


from django.contrib.auth.models import User

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)  
    description = models.TextField()
    date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'customer')
