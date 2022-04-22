"""Tests for views in 'cart' app (display items in cart, adjust, remove)"""
from django.test import TestCase
from django.contrib.messages import get_messages
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

    def test_message_displayed_when_item_added(self):
        """Add item, confirm correct success message is displayed"""
        response = self.client.post('/cart/add/1', {
            'quantity': 1,
            'redirect_url': '/products/1'
        })
        self.assertRedirects(response, '/products/1')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, 'show_bag_in_toast success')
        self.assertEqual(
            messages[0].message,
            'Large Wall Hanging added to your bag'
            )

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

    def test_message_displayed_when_item_added_again(self):
        """
        Add item, then add the same item again
        Confirm correct success message is displayed
        """
        response = self.client.post('/cart/add/1', {
            'quantity': 1,
            'redirect_url': '/products/1'
        })
        self.assertRedirects(response, '/products/1')
        response = self.client.post('/cart/add/1', {
            'quantity': 1,
            'redirect_url': '/products/1'
        })
        self.assertRedirects(response, '/products/1')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, 'show_bag_in_toast success')
        self.assertEqual(
            messages[0].message,
            'Quantity for Large Wall Hanging updated to 2'
            )

    def test_cannot_add_same_item_if_total_quantity_will_exceed_max(self):
        """
        Add item to cart that is already in cart with a quantity that will
        bring total for that item above the max of 10. Cart should not update
        and an error message should be shown.
        """
        self.client.post('/cart/add/1', {
            'quantity': 3,
            'redirect_url': '/products/1'
        })
        response = self.client.get('/cart/')
        cart_item = response.context['cart_items'][0]
        self.assertEqual(cart_item['quantity'], 3)
        response = self.client.post('/cart/add/1', {
            'quantity': 8,
            'redirect_url': '/products/1'
        })
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, 'error')
        self.assertEqual(
            messages[0].message,
            'As these are handmade items, I only sell a max of 10 of each at '
            'a time. You have 3 of "Large Wall Hanging" in your bag and '
            'adding another 8 will bring total quantity for that item above '
            '10. Thank you for your interest but please reduce the quantity '
            'and try again. Thank you!'
            )
        response = self.client.get('/cart/')
        cart_item = response.context['cart_items'][0]
        self.assertEqual(cart_item['quantity'], 3)


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

    def test_message_displayed_when_quantity_increased(self):
        """
        Add an item to the cart. Then go to cart and adjust the
        quantity. Confirm success message is correct.
        """
        response = self.client.post('/cart/add/1', {
            'quantity': 1,
            'redirect_url': '/products/1'
        })
        self.client.get('/cart/')
        response = self.client.post('/cart/adjust/1', {
            'quantity': 4,
        })
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, 'show_bag_in_toast success')
        self.assertEqual(
            messages[0].message,
            'Quantity for Large Wall Hanging updated to 4'
            )

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

    def test_msg_shown_when_quantity_reduced_to_zero(self):
        """
        Add an item to the cart. Then go to cart and adjust the
        quantity to zero. Confirm success message is correct.
        """
        response = self.client.post('/cart/add/1', {
            'quantity': 1,
            'redirect_url': '/products/1'
        })
        self.client.get('/cart/')
        response = self.client.post('/cart/adjust/1', {
            'quantity': 0,
        })
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, 'show_bag_in_toast success')
        self.assertEqual(
            messages[0].message,
            'Large Wall Hanging removed from your bag'
            )


class TestRemoveFromView(TestCase):
    """Test remove_from_cart view - triggered by script that posts the url"""
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

    def test_item_is_removed(self):
        """
        Add item to cart, confirm there is one item in cart.
        Then remove the item, check response successful,
        go to cart page and check cart is empty.
        """
        response = self.client.post('/cart/add/1', {
            'quantity': 1,
            'redirect_url': '/products/1'
        })
        response = self.client.get('/cart/')
        self.assertEqual(len(response.context['cart_items']), 1)
        response = self.client.post('/cart/remove/1/', {})
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/cart/')
        self.assertEqual(len(response.context['cart_items']), 0)

    def test_msg_shown_when_item_is_removed(self):
        """
        Add an item to the cart. Then go to cart and remove the
        item. Confirm success message is correct.
        """
        response = self.client.post('/cart/add/1', {
            'quantity': 1,
            'redirect_url': '/products/1'
        })
        self.client.get('/cart/')
        response = self.client.post('/cart/remove/1/', {})
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, 'show_bag_in_toast success')
        self.assertEqual(
            messages[0].message,
            'Large Wall Hanging removed from your bag'
            )

    def test_error_msg_shown_when_exception_raised(self):
        """
        Post to remove from cart url without any items in the cart
        Confirm error message is raised.
        """
        self.client.get('/cart/')
        response = self.client.post('/cart/remove/1/', {})
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, 'error')
        self.assertEqual(
            messages[0].message,
            "Error removing item: '1'"
            )
