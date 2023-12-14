from rest_framework import serializers
from .models import Product, Customer, Review
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


