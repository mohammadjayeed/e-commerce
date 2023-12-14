from django.shortcuts import render
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from .models import Customer, Product, Review
from .serializers import CustomerSerializer, ProductSerializer, ReviewSerializer
from .permissions import IsAdminOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
# Create your views here.


class ProductViewSet(ModelViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
   

    def get_serializer_context(self):
        return {'request': self.request}






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
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # print('+++')
        # print(Review.objects.filter(product_id=self.kwargs['product_pk']))
        return Review.objects.filter(product_id=self.kwargs['product_pk'])
    

    def get_serializer_context(self):
        
        customer = Customer.objects.get(user_id=self.request.user.id)
        return {'product_id': self.kwargs['product_pk'], 'customer_id':customer.id}