"""Tests for views in profiles app"""
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from products.models import Category, Product
from checkout.models import Order
from .models import UserProfile


class TestProfileView(TestCase):
    """Tests for profile view"""
    @classmethod
    def setUpTestData(cls):
        """
        Two test users - second one with information attached to profile.
        Category and Product instance so Order can be created. 2nd user
        attached to the Order instance.
        """
        user1 = User.objects.create_user(
            username='Tester',
            password='SecretCode14',
        )
        user2 = User.objects.create_user(
            username='TesterTwo',
            password='SecretCode14!',
        )
        user1.save()
        user2.save()
        profile = UserProfile.objects.get(id=2)
        profile.default_phone_number = '123456'
        profile.default_street_address1 = 'My Street'
        profile.default_town_or_city = 'My Town'
        profile.save()

        Category.objects.create(
            name='category_and_category',
            friendly_name='Category & Category'
        )

        Product.objects.create(
            category=Category.objects.get(id=1),
            name='product name',
            sku='44444',
            description='product description',
            price=50.00,
        )

        order = Order.objects.create(
            full_name='Name',
            user_profile=UserProfile.objects.get(id=2),
            email='email@email.com',
            phone_number=profile.default_phone_number,
            street_address1=profile.default_street_address1,
            town_or_city=profile.default_town_or_city,
            country='IE',
        )
        order.save()

    def test_redirects_if_not_logged_in(self):
        """
        View restricted to logged in users. Test user redirected to login
        page if not logged in, with redirect to profile page after log in.
        """
        response = self.client.get('/profile/')
        self.assertRedirects(response, '/accounts/login/?next=/profile/')

    def test_correct_url_and_template_used_for_logged_in_user(self):
        """
        login the user and check they can access the page:
        get url for profile page, check the response is 200 (i.e. successful),
        check the correct template is used - profile.html in profiles app
        check user is in the context.
        """
        self.client.login(username='Tester', password='SecretCode14')
        response = self.client.get('/profile/')
        self.assertEqual(str(response.context['user']), 'Tester')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')

    def test_form_is_blank_if_user_has_no_saved_info(self):
        """
        Login the first user who doesn't have info attached to their profile.
        Go to profile page, test that the form fields do not contain any values
        """
        self.client.login(username='Tester', password='SecretCode14')
        response = self.client.get('/profile/')
        self.assertEqual(str(response.context['user']), 'Tester')
        fields = [
            'default_phone_number', 'default_street_address1',
            'default_street_address2', 'default_town_or_city',
            'default_postcode', 'default_county', 'default_country'
            ]
        for field in fields:
            self.assertEqual(response.context['form'][field].value(), None)

    def test_form_contains_users_saved_info(self):
        """
        Login the second user that has info attached to their profile.
        Go to profile page, test that the form fields contain the correct
        information from the profile.
        """
        self.client.login(username='TesterTwo', password='SecretCode14!')
        response = self.client.get('/profile/')
        self.assertEqual(str(response.context['user']), 'TesterTwo')
        self.assertEqual(
            response.context['form']['default_phone_number'].value(),
            '123456'
            )
        self.assertEqual(
            response.context['form']['default_street_address1'].value(),
            'My Street'
            )
        self.assertEqual(
            response.context['form']['default_town_or_city'].value(),
            'My Town'
            )

    def test_can_update_profile_information(self):
        """
        Go to profile and verify existing data in the profile form.
        Test that posting the profile form with updated information works and
        the default information in the form is the updated values.
        """
        self.client.login(username='TesterTwo', password='SecretCode14!')
        response = self.client.get('/profile/')
        self.assertEqual(
            response.context['form']['default_phone_number'].value(),
            '123456'
            )
        self.assertEqual(
            response.context['form']['default_street_address1'].value(),
            'My Street'
            )
        self.assertEqual(
            response.context['form']['default_town_or_city'].value(),
            'My Town'
            )
        self.client.post('/profile/', {
            'default_phone_number': '123456789',
            'default_street_address1': 'My new Street',
            'default_town_or_city': 'My new Town',
            })
        response = self.client.get('/profile/')
        self.assertEqual(
            response.context['form']['default_phone_number'].value(),
            '123456789'
            )
        self.assertEqual(
            response.context['form']['default_street_address1'].value(),
            'My new Street'
            )
        self.assertEqual(
            response.context['form']['default_town_or_city'].value(),
            'My new Town'
            )

    def test_success_msg_shown_when_profile_updated(self):
        """
        Test that the success message is generated after posting the form
        and that the msg is as expected.
        """
        self.client.login(username='TesterTwo', password='SecretCode14!')
        response = self.client.post('/profile/', {
            'default_phone_number': '123456789',
            'default_street_address1': 'My new Street',
            'default_town_or_city': 'My new Town',
            })
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, 'success')
        self.assertEqual(
            messages[0].message,
            'Your profile information was updated.'
            )

    def test_zero_orders_in_context_for_user_with_no_orders(self):
        """
        Login user who doesn't have any orders. Go to profile page, confirm
        length of orders in context is 0 and that the message stating they
        have no orders is in the html.
        """
        self.client.login(username='Tester', password='SecretCode14')
        response = self.client.get('/profile/')
        self.assertEqual(str(response.context['user']), 'Tester')
        self.assertEqual(len(response.context['orders']), 0)
        self.assertContains(
            response,
            '<p class="fw-600 mb-5">You don\'t have any previous orders '
            'to be displayed yet.</p>'
            )

    def test_order_history_shown_for_user_wtih_previous_orders(self):
        """
        Login the second user that has an order saved to their profile.
        Go to profile page, test that user_profile on the order matches this
        user, and that there is one order in the context (one created in setUp)
        """
        self.client.login(username='TesterTwo', password='SecretCode14!')
        response = self.client.get('/profile/')
        self.assertEqual(str(response.context['user']), 'TesterTwo')
        self.assertTrue('orders' in response.context)
        for order in response.context['orders']:
            self.assertEqual(response.context['user'], order.user_profile.user)
        self.assertEqual(len(response.context['orders']), 1)
