"""Tests for views in 'cart' app (display items in cart, adjust, remove)"""
from django.test import TestCase
from products.models import Category, Product


class TestViewCartView(TestCase):
    """To test the view_cart view - page displaying items in cart"""

    def test_correct_url_and_template_used(self):
        """
        get the url for cart page, check the response is 200 (i.e. successful)
        check the correct template is used - cart.html in cart app
        """
        response = self.client.get('/cart/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/cart.html')


class TestAddToCartView(TestCase):
    """To test the add_to_cart view - form posting item to cart"""
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

    def test_can_add_item_to_cart(self):
        """
        Test add to cart - go to cart page, confirm no items in cart
        Post the add to cart form, verify the page redirects correctly
        Go to the cart page again and check 1 item now in cart
        Check name of product in cart is correct
        """
        response = self.client.get('/cart/')
        self.assertEqual(len(response.context['cart_items']), 0)
        response = self.client.post('/cart/add/1', {
            'quantity': 1,
            'redirect_url': '/products/1'
        })
        self.assertRedirects(response, '/products/1')
        response = self.client.get('/cart/')
        self.assertEqual(len(response.context['cart_items']), 1)
        cart = response.context['cart_items'][0]
        self.assertEqual(cart['product'].name, 'Large Wall Hanging')

    def test_quantity_updates_when_adding_an_existing_item_to_cart(self):
        """
        Test add item to cart that is already in cart, quantity should update
        Starting with empty cart, post add to cart form, verify item in cart
        and qty is 1.
        Post add to cart form again with same item, verify that length of
        context is still 1 (i.e. still 1 item id) but quantity of item is 2.
        """
        response = self.client.get('/cart/')
        self.assertEqual(len(response.context['cart_items']), 0)
        response = self.client.post('/cart/add/1', {
            'quantity': 1,
            'redirect_url': '/products/1'
        })
        response = self.client.get('/cart/')
        self.assertEqual(len(response.context['cart_items']), 1)
        cart_item = response.context['cart_items'][0]
        self.assertEqual(cart_item['product'].name, 'Large Wall Hanging')
        self.assertEqual(cart_item['quantity'], 1)
        response = self.client.post('/cart/add/1', {
            'quantity': 1,
            'redirect_url': '/products/1'
        })
        response = self.client.get('/cart/')
        self.assertEqual(len(response.context['cart_items']), 1)
        cart_item = response.context['cart_items'][0]
        self.assertEqual(cart_item['product'].name, 'Large Wall Hanging')
        self.assertEqual(cart_item['quantity'], 2)


class TestAdjustCartView(TestCase):
    """To test the adjust_cart view - form posting adjusted quantity"""
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

    def test_item_quantity_is_updated(self):
        """
        Add item to cart, then adjust quantity, check page redirects.
        Check quantity of item in cart was updated
        """
        response = self.client.post('/cart/add/1', {
            'quantity': 1,
            'redirect_url': '/products/1'
        })
        response = self.client.get('/cart/')
        self.assertEqual(len(response.context['cart_items']), 1)
        response = self.client.post('/cart/adjust/1', {
            'quantity': 4,
        })
        self.assertRedirects(response, '/cart/')
        response = self.client.get('/cart/')
        self.assertEqual(len(response.context['cart_items']), 1)
        cart_item = response.context['cart_items'][0]
        self.assertEqual(cart_item['quantity'], 4)

    def test_item_is_removed_if_quantity_is_zero(self):
        """
        Add item to cart, confirm there is one item in cart.
        Then adjust quantity to 0, check page redirects, check cart is empty.
        """
        response = self.client.post('/cart/add/1', {
            'quantity': 1,
            'redirect_url': '/products/1'
        })
        response = self.client.get('/cart/')
        self.assertEqual(len(response.context['cart_items']), 1)
        response = self.client.post('/cart/adjust/1', {
            'quantity': 0,
        })
        self.assertRedirects(response, '/cart/')
        response = self.client.get('/cart/')
        self.assertEqual(len(response.context['cart_items']), 0)
