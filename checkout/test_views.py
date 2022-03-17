"""Tests for Views in the checkout app"""
from django.test import TestCase
from django.contrib.messages import get_messages
from products.models import Product, Category


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
