from django.test import TestCase
from decimal import Decimal
from datetime import datetime
from django.contrib.auth.models import User
from .models import Product, Customer, Order, OrderItem, Review, Cart, CartItem
from datetime import date
from uuid import uuid4
from django.db.utils import IntegrityError

class ProductModelTestCase(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            title='Product A',
            description='This is a Product A',
            unit_price=Decimal('9.99'),
            inventory=10
        )

    def test_product_creation(self):
        self.assertEqual(self.product.title, 'Product A')
        self.assertEqual(self.product.description, 'This is a Product A')
        self.assertEqual(self.product.unit_price, Decimal('9.99'))
        self.assertEqual(self.product.inventory, 10)
        self.assertIsInstance(self.product.last_update, datetime)

    def test_inventory_update(self):
        new_inventory = 5
        self.product.inventory_update(new_inventory)
        self.assertEqual(self.product.inventory, new_inventory)

    def test_str_representation(self):
        self.assertEqual(str(self.product), 'Product A')


class CustomerModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user_test', password='password_test')
        self.customer = Customer.objects.get(user=self.user)

    def test_customer_creation(self):
        
        customer = Customer.objects.get(user=self.user)
        # Update the customer fields
        customer.phone = '1234567890'
        customer.birth_date = date(1990, 1, 1)
        customer.save()

        # Refresh the customer instance to get the updated data from the database
        updated_customer = Customer.objects.get(user=self.user)

        # Assert the updated values
        self.assertEqual(updated_customer.phone, '1234567890')
        self.assertEqual(updated_customer.birth_date, date(1990, 1, 1))
        self.assertEqual(updated_customer.user, self.user)
        

    

    def test_str_representation(self):
        self.assertEqual(str(self.customer), 'Customer {}'.format(self.customer.id))

    
class OrderModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user_test', password='password_test')
        self.customer = Customer.objects.get(user=self.user)
        self.order = Order.objects.create(
            status=Order.STATUS_PENDING,
            customer=self.customer
        )

    def test_order_creation(self):
        self.assertEqual(self.order.status, Order.STATUS_PENDING)
        self.assertEqual(self.order.customer, self.customer)

    def test_default_status(self):
        default_order = Order.objects.create(customer=self.customer)
        self.assertEqual(default_order.status, Order.STATUS_PENDING)

    def test_placed_at_auto_now_add(self):
        self.assertIsNotNone(self.order.placed_at)

    def test_customer_foreign_key(self):
        self.assertEqual(self.order.customer, self.customer)
        self.assertEqual(self.order.customer.user, self.user)
        

class OrderItemModelTestCase(TestCase):
    def setUp(self):

        self.user = User.objects.create_user(username='user_test', password='password_test')
        self.customer = Customer.objects.get(user=self.user)


        self.order = Order.objects.create(status=Order.STATUS_PENDING, customer=self.customer)
        
        self.product = Product.objects.create(
            title='Product A',
            description='This is a Product A',
            unit_price=Decimal('13.80'),
            inventory=2
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            unit_price=13.80
        )

    def test_order_item_creation(self):
        self.assertEqual(self.order_item.order, self.order)
        self.assertEqual(self.order_item.product, self.product)
        self.assertEqual(self.order_item.quantity, 2)
        self.assertEqual(self.order_item.unit_price, 13.80)


class CartModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user_test', password='password_test')
        self.cart = Cart.objects.create()

    def test_cart_creation(self):
        self.assertTrue(str(self.cart.id), uuid4().hex)
        self.assertIsNotNone(self.cart.created_at)

class CartItemModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user_test', password='password_test')
        self.cart = Cart.objects.create()
        self.product = Product.objects.create(
            title='Product A',
            description='This is a Product A',
            unit_price=13.80,
            inventory=10
        )
        self.cart_item = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=2
        )

    def test_cart_item_creation(self):
        self.assertEqual(self.cart_item.cart, self.cart)
        self.assertEqual(self.cart_item.product, self.product)
        self.assertEqual(self.cart_item.quantity, 2)

    def test_unique_together_constraint_violation(self):
        with self.assertRaises(Exception):
            CartItem.objects.create(
                cart=self.cart,
                product = self.product,
                quantity=3
            )

class ReviewModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user_test', password='password_test')
        self.customer = Customer.objects.get(user=self.user)
        self.product = Product.objects.create(
            title='Product A',
            description='This is a Product A',
            unit_price=Decimal('9.99'),
            inventory=10
        )
        self.review = Review.objects.create(
            product=self.product,
            customer=self.customer,
            description='This is a test review'
        )

    def test_review_creation(self):
        self.assertEqual(self.review.product, self.product)
        self.assertEqual(self.review.customer, self.customer)
        self.assertEqual(self.review.description, 'This is a test review')
        self.assertIsNotNone(self.review.date)

    def test_unique_together_constraint(self):
        with self.assertRaises(IntegrityError):
            Review.objects.create(
                product=self.product,
                customer=self.customer,
                description='Another test review'
            )