"""Tests for models in checkout app"""
from decimal import Decimal
from django.test import TestCase
from products.models import Product, Category
from .models import Order, OrderLineItem


class TestOrderModel(TestCase):
    """Tests for Order model"""

    @classmethod
    def setUpTestData(cls):
        """
        Create instance of Cagtegory and Order for tests.
        Create 4 instances of Product - prices set as 5, 10, 15 and 20
        """
        Category.objects.create(
            name='category_and_category',
            friendly_name='Category & Category'
        )

        for product in range(4):
            price = 5 * (product + 1)
            Product.objects.create(
                category=Category.objects.get(id=1),
                name=f'product name {product}',
                sku=f'44444{product}',
                description='product description',
                price=price,
            )

        Order.objects.create(
            full_name='Name',
            email='email@email.com',
            phone_number='12345678',
            street_address1='My street',
            town_or_city='My town',
            country='IE',
        )

    def test_update_total_method_calculates_totals_with_delivery(self):
        """
        Add items to Order instance, setting the quantity as 1 of product 1,
        and 2 of product 2. So total price for each line item:
        item1: 1*5=5 and item2: 2*10=20, giving order total 25, delivery 10%
        """
        for item in range(2):
            quantity = 2 if item % 2 else 1
            OrderLineItem.objects.create(
                order=Order.objects.get(id=1),
                product=Product.objects.get(id=int(item+1)),
                quantity=quantity,
            )
        order = Order.objects.get(id=1)
        self.assertEqual(order.order_total, 25.00)
        self.assertEqual(order.delivery_cost, 2.50)
        self.assertEqual(order.grand_total, 27.50)

    def test_update_total_method_calculates_totals_no_delivery(self):
        """
        Add items to Order instance, set quantity as 1 of products 1 + 3,
        and 2 of products 2 + 4. So total price for each line item:
        item1: 1*5=5, item2: 2*10=20, item3: 1*15=15, item4: 2*20=40,
        giving order total 80, no delivery as above delivery threshold
        """
        for item in range(4):
            quantity = 2 if item % 2 else 1
            OrderLineItem.objects.create(
                order=Order.objects.get(id=1),
                product=Product.objects.get(id=int(item+1)),
                quantity=quantity,
            )
        order = Order.objects.get(id=1)
        self.assertEqual(order.order_total, 80.00)
        self.assertEqual(order.delivery_cost, 0.00)
        self.assertEqual(order.grand_total, 80.00)

    def test_string_method_returns_order_number(self):
        """
        Test string method - create order with explicitly set order
        number, confirm this is returned by string method.
        """
        order = Order.objects.create(
            order_number='1234',
            full_name='Name',
            email='email@email.com',
            phone_number='12345678',
            street_address1='My street',
            town_or_city='My town',
            country='IE',
            order_total=123.44,
            delivery_cost=0.00,
            grand_total=123.44,
        )
        self.assertEqual(str(order), '1234')

    def test_save_method_generates_order_number(self):
        """
        Get the order instance created in set up, with no order number.
        Verfiy that there is an order number, of 32 digits.
        """
        order = Order.objects.get(id=1)
        self.assertTrue(order.order_number)
        self.assertEqual(len(order.order_number), 32)


class TestOrderLineItemModel(TestCase):
    """Tests for OrderLineItem model"""
    @classmethod
    def setUpTestData(cls):
        """Create instance of Cagtegory, Product and Order for tests"""
        Category.objects.create(
            name='category_and_category',
            friendly_name='Category & Category'
        )

        Product.objects.create(
            category=Category.objects.get(id=1),
            name='product name',
            sku='44444',
            description='product description',
            price=123.45,
        )

        Order.objects.create(
            full_name='Name',
            email='email@email.com',
            phone_number='12345678',
            street_address1='My street',
            town_or_city='My town',
            country='IE',
        )

    def test_string_method_returns_sku_and_order_number(self):
        """Test string method returns correct details"""
        order_item = OrderLineItem.objects.create(
            order=Order.objects.get(id=1),
            product=Product.objects.get(id=1),
            quantity=1,
        )
        self.assertEqual(
            str(order_item),
            f'SKU 44444 on order {order_item.order.order_number}'
            )

    def test_save_method_sets_lineitem_total_field(self):
        """
        Test lineitem_total is correct after saving instance of model
        lineitem_total is product price*quantity, so 123.45*2 in this test
        """
        order_item = OrderLineItem.objects.create(
            order=Order.objects.get(id=1),
            product=Product.objects.get(id=1),
            quantity=2,
        )
        order_item.save()
        self.assertEqual(order_item.lineitem_total, Decimal('246.90'))
