"""Tests for Views in the checkout app"""
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.conf import settings
from products.models import Product, Category
from profiles.models import UserProfile
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
        test_user = User.objects.create_user(
            username='User',
            password='secret12',
        )
        test_user.save()
        profile = UserProfile.objects.get(id=1)
        profile.default_phone_number = '123456'
        profile.default_street_address1 = 'My Street'
        profile.default_town_or_city = 'Dublin'
        profile.default_postcode = 'AB12345'
        profile.default_county = 'Dublin 1'
        profile.default_country = 'Ireland'
        profile.save()

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

    def test_warning_message_shown_if_stripe_public_key_not_set(self):
        """
        Create cart session variable with items in it.
        Set the STRIPE_PUBLIC_KEY from settins to empty string so it will
        generate the warning message. Go to checkout page, check warning
        msg exists and wording is as expected.
        """
        session = self.client.session
        session['cart'] = {'1': 2}
        session.save()
        settings.STRIPE_PUBLIC_KEY = ''
        response = self.client.get('/checkout/')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, 'warning')
        self.assertEqual(
            messages[0].message,
            'Stripe public key is missing. Did you forget to set it in your '
            'environment?'
            )

    def test_order_form_fields_are_empty_if_user_not_logged_in(self):
        """
        Go to checkout page as an anonymous user, confirm that each field
        on the order form does not have any initial value.
        """
        session = self.client.session
        session['cart'] = {'1': 2}
        session.save()
        response = self.client.get('/checkout/')
        form = response.context['order_form']
        self.assertFalse(form['full_name'].initial)
        self.assertFalse(form['email'].initial)
        self.assertFalse(form['phone_number'].initial)
        self.assertFalse(form['country'].initial)
        self.assertFalse(form['postcode'].initial)
        self.assertFalse(form['town_or_city'].initial)
        self.assertFalse(form['street_address1'].initial)
        self.assertFalse(form['street_address2'].initial)
        self.assertFalse(form['county'].initial)

    def test_order_form_fields_have_initial_values_if_user_logged_in(self):
        """
        Go to checkout page as an logged in user, confirm that each field
        on the order form has initial values populated from the user profile
        if the data exists on the profile.
        """
        session = self.client.session
        session['cart'] = {'1': 2}
        session.save()
        self.client.login(username='User', password='secret12')
        response = self.client.get('/checkout/')
        form = response.context['order_form']
        self.assertEqual(form['full_name'].initial, 'User')
        self.assertEqual(form['email'].initial, '')
        self.assertEqual(form['phone_number'].initial, '123456')
        self.assertEqual(form['country'].initial, 'Ireland')
        self.assertEqual(form['postcode'].initial, 'AB12345')
        self.assertEqual(form['town_or_city'].initial, 'Dublin')
        self.assertEqual(form['street_address1'].initial, 'My Street')
        self.assertEqual(form['street_address2'].initial, None)
        self.assertEqual(form['county'].initial, 'Dublin 1')

    def test_order_form_fields_empty_if_user_logged_in_but_no_profile(self):
        """
        Create a user (creates a UserProfile instance for them) and log them
        in. Then get their profile and delete it. This means profile will not
        be found when on the checkout page, to populate the orderform.
        Got to checkout page, confirm each field deosn't have initial value.
        """
        session = self.client.session
        session['cart'] = {'1': 2}
        session.save()
        new_user = User.objects.create_user(
            username='Name',
            password='secret123',
        )
        new_user.save()
        self.client.login(username='Name', password='secret123')
        profile = UserProfile.objects.get(user=new_user)
        profile.delete()
        response = self.client.get('/checkout/')
        form = response.context['order_form']
        self.assertFalse(form['full_name'].initial)
        self.assertFalse(form['email'].initial)
        self.assertFalse(form['phone_number'].initial)
        self.assertFalse(form['country'].initial)
        self.assertFalse(form['postcode'].initial)
        self.assertFalse(form['town_or_city'].initial)
        self.assertFalse(form['street_address1'].initial)
        self.assertFalse(form['street_address2'].initial)
        self.assertFalse(form['county'].initial)


class TestCacheCheckoutDataView(TestCase):
    """Tests for the cache_checkout_data view"""
    def test_405_returned_for_get_request(self):
        """
        View restricted to post requests. Ensure 405 (method not allowed)
        is raised on a get request.
        """
        response = self.client.get('/checkout/cache_checkout_data/')
        self.assertEqual(response.status_code, 405)

    def test_400_returned_and_error_message_shown_if_error(self):
        """
        Post to the view with an error, test response is 400 and
        error message shown and correct.
        """
        response = self.client.post('/checkout/cache_checkout_data/', {
            'save_info': False,
        })
        self.assertEqual(response.status_code, 400)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, 'error')
        self.assertEqual(
            messages[0].message,
            'Sorry, your payment cannot be processed right now. '
            'Please try again later.'
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
