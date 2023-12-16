from django.shortcuts import render
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from .models import Customer, Product, Review, Cart, CartItem, Order
from .serializers import (CustomerSerializer, ProductSerializer, ReviewSerializer, CartSerializer, CartItemSerializer, 
AddCartItemSerializer, UpdateCartItemSerializer, OrderSerializer, CreateOrderSerializer, UpdateOrderSerializer)
from .permissions import IsAdminOrReadOnly, ReviewOwnerOrAdminOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.permissions import BasePermission, IsAdminUser
# Create your views here.


class ProductViewSet(ModelViewSet):
    """
    API View function :
    
    This viewset provides `list`, `create`, `retrieve`,
    `update`, and `destroy` actions.

    Only Admin can perform the actions, otherwise its read only

    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'pk'
   

class CustomerViewSetAPI(GenericViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    # permission_classes = [IsAuthenticated]


    @action(detail=False, methods=['GET','PUT','DELETE'], permission_classes=[IsAuthenticated])
    def me(self,request):
        (customer,created) = Customer.objects.get_or_create(user_id=request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer,data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        elif request.method == 'DELETE':
            customer.delete()
            return Response({'message': 'Customer deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        

class ReviewViewSet(ModelViewSet):
    """
    API View function :
    
    This viewset provides per customer - single review uniqueness. 
    A single product can be reviewed multiples times by different users.
    A single user cannot review the same product multiple times


    Only authenticated customers can perform actions or else
    anonymous users can view only

    """
    serializer_class = ReviewSerializer
    permission_classes = [ReviewOwnerOrAdminOrReadOnly]
    

    def get_queryset(self):

        return Review.objects.filter(product_id=self.kwargs['product_pk'])
    

    def get_serializer_context(self):
        try:
            customer = Customer.objects.get(user_id=self.request.user.id)
        except Customer.DoesNotExist:
            return
        return {'product_id': self.kwargs['product_pk'], 'customer_id':customer.id}
    
class CartViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):

    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer

class CartItemViewSet(ModelViewSet):

    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']).select_related('product')
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer
    
    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}
    
class OrderViewSet(ModelViewSet):
    
    
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    # Here CreateModelMixin (ModelViewSet inherits CreateModelMixin alongside other mixins) is overwritten by custom create method 
    # in order to generate a proper response to be sent to the client end
    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(data=request.data,context={'user_id': self.request.user.id})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def get_serializer_class(self):

        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Order.objects.all()

        customer_id = Customer.objects.only('id').get(user_id=user.id)
        return Order.objects.filter(customer_id=customer_id)