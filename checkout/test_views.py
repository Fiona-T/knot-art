"""Tests for Views in the checkout app"""
from django.test import TestCase
from django.contrib.messages import get_messages
from products.models import Product, Category
from .models import Order


class TestCheckoutView(TestCase):
    """Tests for the checkout view"""
    @classmethod
    def setUp(cls):
        """
        Create instance of Category and Product for test
        """
        Category.objects.create(
            name='category_name',
            friendly_name='Category'
        )
        Product.objects.create(
            category=Category.objects.get(id=1),
            name='Large Wall Hanging',
            sku='12345',
            description='product description',
            price=123.45,
            is_active=True,
        )

    def test_correct_url_and_template_used_if_items_in_cart(self):
        """
        add item to the cart (as page will only show if cart not empty),
        get url for checkout page, check the response is 200 (i.e. successful),
        check the correct template is used - checkout.html in checkout app
        """
        self.client.post('/cart/add/1', {
            'quantity': 1,
            'redirect_url': '/products/1'
        })
        response = self.client.get('/checkout/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout.html')

    def test_redirects_and_error_msg_shown_if_no_items_in_cart(self):
        """
        go to checkout page without adding any items to cart,
        check the page redirects and the correct error msg is shown.
        """
        response = self.client.get('/checkout/')
        self.assertRedirects(response, '/products/')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, 'error')
        self.assertEqual(
            messages[0].message,
            "Can't checkout as you don't have anything in your bag at the "
            "moment! Add some items and try again."
            )


class TestCheckoutSuccessView(TestCase):
    """Tests for the checkout view"""
    @classmethod
    def setUp(cls):
        """
        Create instance of Category and Product for test
        """
        Category.objects.create(
            name='category_name',
            friendly_name='Category'
        )
        Product.objects.create(
            category=Category.objects.get(id=1),
            name='Large Wall Hanging',
            sku='12345',
            description='product description',
            price=123.45,
            is_active=True,
        )

    def test_correct_url_and_template_used(self):
        """
        create an order, get url for checkout success page using order number
        check the response is 200 (i.e. successful),
        check correct template is used - checkout_success.html in checkout app
        """
        order = Order.objects.create(
            full_name='Name',
            email='email@email.com',
            phone_number='12345678',
            street_address1='My street',
            town_or_city='My town',
            country='IE',
        )
        response = self.client.get(
            f'/checkout/checkout_success/{order.order_number}'
            )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout_success.html')

    def test_message_displayed_and_contents_correct(self):
        """
        create an order, go to checkout success page using order number
        check message exists, is success msg and has correct content
        """
        order = Order.objects.create(
            full_name='Name',
            email='email@email.com',
            phone_number='12345678',
            street_address1='My street',
            town_or_city='My town',
            country='IE',
        )
        response = self.client.get(
            f'/checkout/checkout_success/{order.order_number}'
            )
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, 'success')
        self.assertEqual(
            messages[0].message,
            f'Order number: {order.order_number} successfully created! '
            'An email will be sent to email@email.com with the order details.'
            )

    def test_cart_session_variable_is_deleted(self):
        """
        add an item to cart, confirm the cart session variable is equal to a
        dict containing item id and quantity.
        Create an order, go to checkout success page using order number.
        Check that trying to access the 'cart' session variable raises a
        KeyError - which shows that the variable was deleted
        """
        self.client.post('/cart/add/1', {
            'quantity': 1,
            'redirect_url': '/products/1'
        })
        cart = self.client.session['cart']
        self.assertEqual(cart, {'1': 1})
        order = Order.objects.create(
            full_name='Name',
            email='email@email.com',
            phone_number='12345678',
            street_address1='My street',
            town_or_city='My town',
            country='IE',
        )
        self.client.get(f'/checkout/checkout_success/{order.order_number}')
        self.assertRaises(KeyError, lambda: self.client.session['cart'])
