"""Tests for views in 'product' app (shop)"""
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Category, Product


class TestShowProductsView(TestCase):
    """To test the show_products view - shop page displaying products"""
    @classmethod
    def setUp(cls):
        """
        Create instance of Category
        Create 7 instances of Product, 3 active and 4 inactive
        """
        Category.objects.create(
            name='category_name',
            friendly_name='Category'
        )
        number_of_products = 7
        for product in range(number_of_products):
            is_active = True if product % 2 else False
            Product.objects.create(
                category=Category.objects.get(id=1),
                name=f'product number {product}',
                sku='12345',
                description='product description',
                price=123.45,
                is_active=is_active,
                is_new=True
            )

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
        Check view returns 3 products i.e. the active ones created in setUp
        Check that for each product in the context, the is_active flag is True
        """
        response = self.client.get('/products/')
        self.assertTrue('products' in response.context)
        self.assertEqual(len(response.context['products']), 3)
        for product in response.context['products']:
            self.assertTrue(product.is_active)

    def test_all_products_displayed_for_superuser(self):
        """
        Create a superuser, log them in
        Check view returns 7 products i.e. all including active + not active
        Check that for each product in the context, the is_active flag is True
        """
        test_superuser = User.objects.create_user(
            username='admin',
            password='secret',
            is_superuser=True
        )
        test_superuser.save()

        self.client.login(username='admin', password='secret')
        response = self.client.get('/products/')
        self.assertTrue('products' in response.context)
        self.assertEqual(len(response.context['products']), 7)

    def test_search_returns_product_matching_search_term_in_name(self):
        """
        Test that searching returns products where search term in name.
        Create a new product in addition to those in setUp.
        Check that products page initially contains 4 products.
        Search for a word contained in new product name, verifiy the response
        now contains just one product and the name matches that product.
        """
        Product.objects.create(
            category=Category.objects.get(id=1),
            name='Large Wall Hanging',
            sku='12345',
            description='product description',
            price=123.45,
            is_active=True,
            is_new=True
        )
        response = self.client.get('/products/')
        self.assertEqual(len(response.context['products']), 4)
        response = self.client.get('/products/?q=large')
        self.assertEqual(len(response.context['products']), 1)
        self.assertEqual(
            response.context['products'][0].name, 'Large Wall Hanging'
            )

    def test_search_returns_product_matching_search_term_in_description(self):
        """
        Test that searching returns products where search term in description.
        Create a new product in addition to those in setUp.
        Check that products page initially contains 4 products.
        Search for word contained in new product description, verifiy response
        now contains one product and it is the new product.
        Search for word contained in 4 products, verify 4 products returned.
        """
        Product.objects.create(
            category=Category.objects.get(id=1),
            name='Large Wall Hanging',
            sku='12345',
            description='specific product description',
            price=123.45,
            is_active=True,
            is_new=True
        )
        response = self.client.get('/products/')
        self.assertEqual(len(response.context['products']), 4)
        response = self.client.get('/products/?q=specific')
        self.assertEqual(len(response.context['products']), 1)
        self.assertEqual(
            response.context['products'][0].description,
            'specific product description'
            )
        response = self.client.get('/products/?q=description')
        self.assertEqual(len(response.context['products']), 4)


class TestProductDetailsView(TestCase):
    """Test product details view - page showing individual product in shop"""
    @classmethod
    def setUp(cls):
        """Create instance of Category, two instances of Product for tests"""
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

    def test_correct_url_and_template_used(self):
        """
        get the url for product details page using id of 1st test Product
        instance, Check the response is 200 (i.e. successful)
        Check correct template is used - product_details.html in products app
        """
        response = self.client.get('/products/1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_details.html')

    def test_correct_product_is_displayed(self):
        """
        Check product name in context matches that of first product instance
        (ie. page is displaying the correct product)
        """
        response = self.client.get('/products/1')
        product = response.context['product']
        self.assertEqual(product.name, 'product name')

    def test_superuser_can_view_inactive_product(self):
        """
        Create superuser and log them in.
        Go to product detail url for 2nd product instance (not active)
        Check response code is 200, successful
        Check the is_active flag for that product is false
        """
        test_superuser = User.objects.create_user(
            username='admin',
            password='secret',
            is_superuser=True
        )
        test_superuser.save()

        self.client.login(username='admin', password='secret')
        response = self.client.get('/products/2')
        self.assertEqual(response.status_code, 200)
        product = response.context['product']
        self.assertFalse(product.is_active)

    def test_non_superuser_cannot_view_inactive_product(self):
        """
        Get product with id of 2, confirm it is not active
        Go to product detail url for this product
        Check response code is 404, as only superuser can access
        """
        product = Product.objects.get(id=2)
        self.assertFalse(product.is_active)
        response = self.client.get('/products/2')
        self.assertEqual(response.status_code, 404)
