from rest_framework import serializers
from .models import Product, Customer, Review, Cart, CartItem
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    user_id  = serializers.IntegerField(read_only=True)
    class Meta:
        model = Customer
        fields = ['id','user_id','phone','birth_date']


class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField(required=False)
    class Meta:
        model = Review
        fields = ['id','username', 'date', 'description']

    def get_username(self, obj):
        return obj.customer.user.username if obj.customer else None

    def create(self, validated_data):
        product_id = self.context['product_id']
        customer_id= self.context['customer_id']
        
        # print(product_id)
        # print(customer_id)
        # print(Review.objects.filter(product_id=product_id, customer_id=customer_id).exists())
        if Review.objects.filter(product_id=product_id, customer_id=customer_id).exists():
            raise ValidationError(detail={'review_status': ['Already reviewed by user']})
        return Review.objects.create(product_id=product_id, customer_id=customer_id, **validated_data)
    
class CustomProductInCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','title','description','unit_price']

class CartItemSerializer(serializers.ModelSerializer):
    product = CustomProductInCartSerializer()
    price_in_total = serializers.SerializerMethodField()

    def get_price_in_total(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.unit_price
    
    class Meta:
        model = CartItem
        fields = ['id','product','quantity','price_in_total']

class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True,read_only=True)
    total_cart_price = serializers.SerializerMethodField()

    def get_total_cart_price(self, cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])

    class Meta:
        model = Cart
        fields = ['id','items','total_cart_price']

