"""Tests for views in 'product' app (shop)"""
from django.test import TestCase
from .models import Category, Product


class TestShowProductsView(TestCase):
    """To test the show_products view - shop page displaying products"""
    def test_correct_url_and_template_used(self):
        """
        get the url for shop page, check the response is 200 (i.e. successful)
        check the correct template is used - products.html in products app
        """
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')

    def test_only_active_products_displayed(self):
        """
        Create category instance and two product instances, one active, one not
        Check that the view only returns one product i.e. the active one
        Check that for each product in the context, the is_active flag is True
        """
        Category.objects.create(
            name='category_name',
            friendly_name='Category'
        )
        Product.objects.create(
            category=Category.objects.get(id=1),
            name='product name',
            sku='12345',
            description='product description',
            price=123.45,
            is_active=True,
            is_new=True
        )
        Product.objects.create(
            category=Category.objects.get(id=1),
            name='different name',
            sku='12345',
            description='product description',
            price=123.45,
            is_active=False,
            is_new=True
        )
        response = self.client.get('/products/')
        self.assertTrue('products' in response.context)
        self.assertEqual(len(response.context['products']), 1)
        for product in response.context['products']:
            self.assertTrue(product.is_active)
