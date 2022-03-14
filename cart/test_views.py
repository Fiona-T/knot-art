"""Tests for views in 'cart' app (display items in cart, adjust, remove)"""
from django.test import TestCase


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
