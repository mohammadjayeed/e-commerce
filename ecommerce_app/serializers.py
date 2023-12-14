from rest_framework import serializers
from .models import Product, Customer, Review, Cart, CartItem, Order, OrderItem
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.db import transaction
from django.db.models import F

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

class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No product with the id exists.')
        return value

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        try:
            product = Product.objects.get(id=product_id)
            inventory_check = product.inventory - quantity 
            

            if inventory_check < 0:
                raise ValidationError('Desired quantity not present in stock')

            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item

        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)

        return self.instance

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']



class CartSerializer(serializers.ModelSerializer):
    
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True,read_only=True)
    total_cart_price = serializers.SerializerMethodField()

    def get_total_cart_price(self, cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])

    class Meta:
        model = Cart
        fields = ['id','items','total_cart_price']


class OrderItemSerializer(serializers.ModelSerializer):
    product = CustomProductInCartSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'unit_price', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ['id','customer','placed_at','status','items']

class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()


    # Checking if the cart id is a valid cart id by checking the database
    # Also checking if the cart is empty in the second if statement
    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError('Cart ID was not found.')
        if CartItem.objects.filter(cart_id=cart_id).count() == 0:
            raise serializers.ValidationError('Empty Cart.')
        return cart_id
    

    def save(self, **kwargs):

        with transaction.atomic():
            cart_id = self.validated_data['cart_id']
            customer = Customer.objects.get(user_id=self.context['user_id'])
            order = Order.objects.create(customer=customer)

            cart_items = CartItem.objects.select_related('product').filter(cart_id=cart_id)


            order_items = []
            for item in cart_items:
                order_item = OrderItem(
                    order=order,
                    product=item.product,
                    unit_price=item.product.unit_price,
                    quantity=item.quantity
                )
                
                

                Product.objects.get(pk=item.product.id).inventory_update(inventory=F('inventory') - (item.product.inventory- item.quantity))

                order_items.append(order_item)


            OrderItem.objects.bulk_create(order_items)

            # Deleting cart object for successfully placed order
            Cart.objects.filter(pk=cart_id).delete()

            # purpose of this order return is to manipulate it further in the createmodelmixin and thus generating proper
            # reponse to be sent to the client
            return order

class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['payment_status']