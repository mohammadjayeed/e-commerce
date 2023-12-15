from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from rest_framework.test import force_authenticate
from .views import ProductViewSet, CustomerViewSetAPI, ReviewViewSet, CartViewSet, CartItemViewSet, OrderViewSet
from .models import Product, Customer, Review, Cart, CartItem, Order
from rest_framework import status


class ProductViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='admin', password='admin123',is_staff=True)
        self.viewset = ProductViewSet.as_view({'get': 'list', 'post': 'create', 'retrieve': 'retrieve', 'put': 'update', 'delete': 'destroy'})
        self.product = Product.objects.create(
            title='Product A',
            description='This is a Product A',
            unit_price=9.99,
            inventory=10
        )

    def test_list_products(self):
        request = self.factory.get('/products/')
        force_authenticate(request, user=self.user)
        response = self.viewset(request)
        self.assertEqual(response.status_code, 200)

    def test_create_product(self):
        request = self.factory.post('/products/', {
            'title': 'New Product',
            'description': 'This is a new product',
            'unit_price': 19.99,
            'inventory': 5
        })
        force_authenticate(request, user=self.user)
        response = self.viewset(request)
        self.assertEqual(response.status_code, 201)

    def test_retrieve_product(self):
        request = self.factory.get(f'/products/{self.product.id}/')
        force_authenticate(request, user=self.user)
        response = self.viewset(request, pk=self.product.id)
        self.assertEqual(response.status_code, 200)

    def test_update_product(self):
        request = self.factory.put(f'/products/{self.product.id}/', {
            'title': 'Updated Product',
            'description': 'This is an updated product',
            'unit_price': 14.99,
            'inventory': 8
        }, content_type='application/json') 
        force_authenticate(request, user=self.user)
        response = self.viewset(request, pk=self.product.id)
        self.assertEqual(response.status_code, 200)

    def test_delete_product(self):
        request = self.factory.delete(f'/products/{self.product.id}/')
        force_authenticate(request, user=self.user)
        response = self.viewset(request, pk=self.product.id)
        self.assertEqual(response.status_code, 204)




class CustomerViewSetAPITestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='admin', password='admin123',is_active=True,is_staff=False)
        self.viewset = CustomerViewSetAPI.as_view({'get': 'me', 'put': 'me', 'delete': 'me'})
        self.customer = Customer.objects.get(user=self.user)

    def test_get_customer(self):
        request = self.factory.get('/customers/me/')
        force_authenticate(request, user=self.user)
        response = self.viewset(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_customer(self):
        request = self.factory.put('/customers/me/', {
            'phone': '01994053942',
            'birth_date': '1991-01-01'
        }, content_type='application/json')
        force_authenticate(request, user=self.user)
        response = self.viewset(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['phone'], '01994053942')
        self.assertEqual(response.data['birth_date'], '1991-01-01')
       
    def test_delete_customer(self):
        request = self.factory.delete('/customers/me/')
        force_authenticate(request, user=self.user)
        response = self.viewset(request)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)



class ReviewViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='jayeed', password='jayeed123', is_active=True, is_staff=False)
        self.viewset = ReviewViewSet.as_view({'get': 'list', 'post': 'create', 'retrieve': 'retrieve', 'put': 'update', 'delete': 'destroy'})
        self.product = Product.objects.create(
            title='Product A',
            description='This is a Product A',
            unit_price=9.99,
            inventory=10
        )
        self.customer = Customer.objects.get(user=self.user)

    def test_list_reviews(self):
        review = Review.objects.create(
            product=self.product,
            customer=self.customer,
            description='Great product!'
        )
        request = self.factory.get(f'/products/{self.product.id}/reviews/')
        force_authenticate(request, user=self.user)
        response = self.viewset(request, product_pk=self.product.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['description'], 'Great product!')

    def test_create_review(self):
        request = self.factory.post(f'/products/{self.product.id}/reviews/', {
            'description': 'Excellent product!'
        })
        force_authenticate(request, user=self.user)
        response = self.viewset(request, product_pk=self.product.id)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['description'], 'Excellent product!')

    def test_retrieve_review(self):
        review = Review.objects.create(
            product=self.product,
            customer=self.customer,
            description='Great product!'
        )
        request = self.factory.get(f'/products/{self.product.id}/reviews/{review.id}/')
        force_authenticate(request, user=self.user)
        response = self.viewset(request, product_pk=self.product.id, pk=review.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual((response.data[0]['description']), 'Great product!')


    def test_update_review(self):
        review = Review.objects.create(
            product=self.product,
            customer=self.customer,
            description='Great product!'
        )
        request = self.factory.put(f'/products/{self.product.id}/reviews/{review.id}/', {
            'description': 'Excellent product!'
        }, content_type='application/json')
        force_authenticate(request, user=self.user)
        response = self.viewset(request, product_pk=self.product.id, pk=review.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['description'], 'Excellent product!')

    def test_delete_review(self):
        review = Review.objects.create(
            product=self.product,
            customer=self.customer,
            description='Great product!'
        )
        request = self.factory.delete(f'/products/{self.product.id}/reviews/{review.id}/')
        force_authenticate(request, user=self.user)
        response = self.viewset(request, product_pk=self.product.id, pk=review.id)
        self.assertEqual(response.status_code, 204)





class CartViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='jayeed', password='admin123', is_staff=False,is_active=True)
        self.viewset = CartViewSet.as_view({'post': 'create', 'get': 'retrieve', 'delete': 'destroy'})
        self.cart = Cart.objects.create()

    def test_create_cart(self):
        request = self.factory.post('/carts/', {})
        force_authenticate(request, user=self.user)
        response = self.viewset(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_cart(self):
        request = self.factory.get(f'/carts/{self.cart.id}/')
        force_authenticate(request, user=self.user)
        response = self.viewset(request, pk=self.cart.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_cart(self):
        request = self.factory.delete(f'/carts/{self.cart.id}/')
        force_authenticate(request, user=self.user)
        response = self.viewset(request, pk=self.cart.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class CartItemViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='admin', password='admin123', is_staff=False)
        self.viewset = CartItemViewSet.as_view({'get': 'list', 'post': 'create', 'patch': 'partial_update', 'delete': 'destroy'})
        self.cart = Cart.objects.create()
        self.product = Product.objects.create(
            title='Product A',
            description='This is a Product A',
            unit_price=9.99,
            inventory=10
        )
        self.cart_item = CartItem.objects.create(
            cart_id=self.cart.id,
            product_id=self.product.id,
            quantity=2
        )

    def test_list_cart_items(self):
        request = self.factory.get('/carts/self.cart.id/items/')
        force_authenticate(request, user=self.user)
        response = self.viewset(request, cart_pk=self.cart.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_cart_item(self):
        request = self.factory.post('/carts/self.cart.id/items/', {
            'product_id': self.product.id,
            'quantity': 3
        })
        force_authenticate(request, user=self.user)
        response = self.viewset(request, cart_pk=self.cart.id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_cart_item(self):
        request = self.factory.patch('/carts/self.cart.id/items/self.cart_item.id/', {
            'quantity': 4
        }, content_type='application/json')
        force_authenticate(request, user=self.user)
        response = self.viewset(request, cart_pk=self.cart.id, pk=self.cart_item.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_cart_item(self):
        request = self.factory.delete('/carts/self.cart.id/items/self.cart_item.id/')
        force_authenticate(request, user=self.user)
        response = self.viewset(request,  cart_pk=self.cart.id, pk=self.cart_item.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class OrderViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='admin', password='admin123', is_staff=True, is_active=True)
        self.viewset = OrderViewSet.as_view({'get': 'list', 'post': 'create', 'patch': 'partial_update', 'delete': 'destroy'})
        self.customer = Customer.objects.get(user=self.user)
        self.order = Order.objects.create(customer_id = self.customer.id)

        self.product = Product.objects.create(
            title='Product A',
            description='This is a Product A',
            unit_price=9.99,
            inventory=10
        )

        self.cart = Cart.objects.create()
        self.cart_item = CartItem.objects.create(
            cart_id=self.cart.id,
            product_id=self.product.id,
            quantity=10
        )

    def test_list_orders(self):
        request = self.factory.get('/orders/')
        force_authenticate(request, user=self.user)
        response = self.viewset(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_order(self):
        request = self.factory.post('/orders/', {
            'cart_id':self.cart.id
        })
        force_authenticate(request, user=self.user)
        response = self.viewset(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_order(self):
        request = self.factory.patch(f'/orders/{self.order.id}/', {
            # Add necessary fields for updating an order
        }, content_type='application/json')
        force_authenticate(request, user=self.user)
        response = self.viewset(request, pk=self.order.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_order(self):
        request = self.factory.delete(f'/orders/{self.order.id}/')
        force_authenticate(request, user=self.user)
        response = self.viewset(request, pk=self.order.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)