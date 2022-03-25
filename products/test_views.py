"""Tests for views in 'product' app (shop)"""
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from .models import Category, Product


class TestShowProductsView(TestCase):
    """To test the show_products view - shop page displaying products"""
    @classmethod
    def setUp(cls):
        """
        Create two instances of Category
        Create 7 instances of Product, 3 active, 4 inactive
        Create 11 instances of Product, 5 category1, 6 category2, all active
        For tests there are: 18 products, 14 active, 4 inactive
        And 8 active in category1, 6 active in category2
        """
        category1 = Category.objects.create(
            name='category_name',
            friendly_name='Category'
        )
        category2 = Category.objects.create(
            name='different_category',
            friendly_name='Category'
        )

        for product in range(7):
            is_active = True if product % 2 else False
            Product.objects.create(
                category=category1,
                name=f'product number {product}',
                sku='12345',
                description='product description',
                price=123.45,
                is_active=is_active,
                is_new=True
            )

        for product in range(11):
            is_active = True if product % 2 else False
            category = category1 if product % 2 else category2
            Product.objects.create(
                category=category,
                name=f'different product number {product}',
                sku='12345',
                description='product description',
                price=123.45,
                is_active=True,
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
        Check view returns 14 products i.e. the active ones created in setUp
        Check that for each product in the context, the is_active flag is True
        """
        response = self.client.get('/products/')
        self.assertTrue('products' in response.context)
        self.assertEqual(len(response.context['products']), 14)
        for product in response.context['products']:
            self.assertTrue(product.is_active)

    def test_all_products_displayed_for_superuser(self):
        """
        Create a superuser, log them in
        Check view returns 18 products i.e. all including active + not active
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
        self.assertEqual(len(response.context['products']), 18)

    def test_search_returns_product_matching_search_term_in_name(self):
        """
        Test that searching returns products where search term in name.
        Create a new product in addition to those in setUp.
        Check that products page initially contains 15 active products.
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
        self.assertEqual(len(response.context['products']), 15)
        response = self.client.get('/products/?q=large')
        self.assertEqual(len(response.context['products']), 1)
        self.assertEqual(
            response.context['products'][0].name, 'Large Wall Hanging'
            )

    def test_search_returns_product_matching_search_term_in_description(self):
        """
        Test that searching returns products where search term in description.
        Create a new product in addition to those in setUp.
        Check that products page initially contains 15 active products.
        Search for word contained in new product description, verifiy response
        now contains one product and it is the new product.
        Search for word contained in 15 products, verify 15 products returned.
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
        self.assertEqual(len(response.context['products']), 15)
        response = self.client.get('/products/?q=specific')
        self.assertEqual(len(response.context['products']), 1)
        self.assertEqual(
            response.context['products'][0].description,
            'specific product description'
            )
        response = self.client.get('/products/?q=description')
        self.assertEqual(len(response.context['products']), 15)

    def test_error_message_displayed_if_no_search_term(self):
        """
        Test that if search box posted without any search terms,
        an error message is displayed. Get the messages, check
        length, tag and content are all as expected.
        """
        response = self.client.get('/products/?q=')
        self.assertRedirects(response, '/products/')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, 'error')
        self.assertEqual(
            messages[0].message,
            "You didn't enter anything in the search box! Try again."
            )

    def test_category_filtering_returns_correct_products(self):
        """
        If category is selected, ensure products match that category
        Check that products page initially contains 14 active products.
        Filter using to category1 name, check 8 products returned
        Filter using to category2 name, check 6 products returned
        """
        response = self.client.get('/products/')
        self.assertEqual(len(response.context['products']), 14)
        response = self.client.get('/products/?category=category_name')
        self.assertEqual(len(response.context['products']), 8)
        for product in response.context['products']:
            self.assertEqual(product.category.name, 'category_name')
        response = self.client.get('/products/?category=different_category')
        self.assertEqual(len(response.context['products']), 6)
        for product in response.context['products']:
            self.assertEqual(product.category.name, 'different_category')

    def test_sort_request_urls_and_context_are_correct(self):
        """
        For sort requests, check that each combination of url is successful
        And that the 'current_sorting' returned in context is correct
        """
        response = self.client.get('/products/')
        self.assertEqual(response.context['current_sorting'], 'None_None')
        sort_options = ['price', 'name']
        for opt in sort_options:
            response = self.client.get(f'/products/?sort={opt}&direction=desc')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.context['current_sorting'], f'{opt}_desc'
                )
        for opt in sort_options:
            response = self.client.get(f'/products/?sort={opt}&direction=asc')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context['current_sorting'], f'{opt}_asc')

    def test_sort_request_order_is_correct(self):
        """
        Test that order of the products returned for a sort request is correct,
        by checking first and last items
        Products created with lowest + highest price and names to test this.
        """
        Product.objects.create(
                category=Category.objects.get(id=1),
                name='a name beginning with a',
                sku='12345',
                description='product description',
                price=555.55,
                is_active=True,
                is_new=True
            )
        Product.objects.create(
                category=Category.objects.get(id=1),
                name='zz later name',
                sku='12345',
                description='product description',
                price=99.00,
                is_active=True,
                is_new=True
            )

        response = self.client.get('/products/?sort=name&direction=asc')
        self.assertEqual(
            response.context['products'][0].name, 'a name beginning with a'
            )
        # have to use len minus 1 here, as negative indexing not supported
        last_item = len(response.context['products'])-1
        self.assertEqual(
            response.context['products'][last_item].name, 'zz later name'
            )
        response = self.client.get('/products/?sort=name&direction=desc')
        self.assertEqual(response.context['products'][0].name, 'zz later name')
        last_item = len(response.context['products'])-1
        self.assertEqual(
            response.context['products'][last_item].name,
            'a name beginning with a'
            )
        response = self.client.get('/products/?sort=price&direction=asc')
        self.assertEqual(float(response.context['products'][0].price), 99.00)
        last_item = len(response.context['products'])-1
        self.assertEqual(
            float(response.context['products'][last_item].price), 555.55
            )
        response = self.client.get('/products/?sort=price&direction=desc')
        self.assertEqual(float(response.context['products'][0].price), 555.55)
        last_item = len(response.context['products'])-1
        self.assertEqual(
            float(response.context['products'][last_item].price), 99.00
            )


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


class TestAddProductView(TestCase):
    """Tests for add_products view"""
    @classmethod
    def setUpTestData(cls):
        """
        Standard user and Superuser for access tests.
        Category and Product for creating new products.
        """
        test_user = User.objects.create_user(
            username='User',
            password='secret12',
        )
        test_user.save()

        test_superuser = User.objects.create_user(
            username='admin',
            password='secret',
            is_superuser=True
        )
        test_superuser.save()

        Category.objects.create(
            name='category_and_category',
            friendly_name='Category & Category'
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

    def test_redirects_if_not_logged_in(self):
        """
        View restricted to logged in users. Test user redirected to login
        page if not logged in, with redirect to add product page after login.
        """
        response = self.client.get('/products/add/')
        self.assertRedirects(response, '/accounts/login/?next=/products/add/')

    def test_403_raised_if_logged_in_but_not_superuser(self):
        """
        View restricted to logged in superusers. Test logged in user who is
        not a superuser gets a 403 response (permission denied)
        """
        self.client.login(username='User', password='secret12')
        response = self.client.get('/products/add/')
        self.assertEqual(response.status_code, 403)

    def test_correct_url_and_template_used_for_logged_in_superuser(self):
        """
        get the url for product details page using id of 1st test Product
        instance, Check the response is 200 (i.e. successful)
        Check correct template is used - product_details.html in products app
        """
        self.client.login(username='admin', password='secret')
        response = self.client.get('/products/add/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/add_product.html')

    def test_can_add_product(self):
        """
        login the admin user, get products url and check length of products is
        one initially (existing product). Then do POST request on add product
        url, with test product. Check redirects to the correct success url
        after adding. Check that length of products is now 2, and name matches.
        """
        self.client.login(username='admin', password='secret')
        response = self.client.get('/products/')
        self.assertEqual(len(response.context['products']), 1)
        response = self.client.post('/products/add/', {
            'category': 1,
            'name': 'new product name',
            'sku': '1234567',
            'description': 'product description new',
            'price': 79.88,
            'is_active': True,
            'is_new': False,
        })
        self.assertRedirects(response, '/products/2')
        response = self.client.get('/products/')
        self.assertEqual(len(response.context['products']), 2)
        self.assertEqual(
            response.context['products'][1].name, 'new product name'
            )

    def test_success_message_displayed_when_product_added(self):
        """Add a product and check msg displayed + is correct"""
        self.client.login(username='admin', password='secret')
        response = self.client.post('/products/add/', {
            'category': 1,
            'name': 'new product name',
            'sku': '1234567',
            'description': 'product description new',
            'price': 79.88,
            'is_active': True,
            'is_new': False,
        })
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, 'success')
        self.assertEqual(
            messages[0].message,
            'New product: new product name added!'
            )

    def test_error_message_displayed_when_form_not_valid(self):
        """
        Attempt to add product with invalid form, and check error msg
        displayed + is correct
        """
        self.client.login(username='admin', password='secret')
        response = self.client.post('/products/add/', {
            'category': 1,
            'name': 'product name',  # same as existing product so form invalid
            'sku': '1234567',
            'description': 'product description new',
            'price': 79.88,
            'is_active': True,
            'is_new': False,
        })
        self.assertFalse(response.context['form'].is_valid())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, 'error')
        self.assertEqual(
            messages[0].message,
            'Product not added. Please check the form for errors and '
            're-submit.'
            )
