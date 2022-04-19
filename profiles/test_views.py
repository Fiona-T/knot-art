"""Tests for views in profiles app"""
import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from products.models import Category, Product
from checkout.models import Order
from markets.models import Market, County
from .models import UserProfile, SavedMarketList


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


class TestPreviousOrderDetailView(TestCase):
    """Tests for previous_order_detail view"""
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
        page if not logged in, with redirect to order history detail page
        after log in.
        """
        order = Order.objects.get(id=1)
        response = self.client.get(
            f'/profile/order_history/{order.order_number}'
            )
        self.assertRedirects(
            response,
            f'/accounts/login/?next=/profile/order_history/'
            f'{order.order_number}'
            )

    def test_correct_url_and_template_used_for_logged_in_user_own_order(self):
        """
        Login the user who is attached to order and check they can access the
        page using the order number. Check the response is 200, check the
        correct template is used - checkout_success.html in checkout app
        """
        order = Order.objects.get(id=1)
        self.client.login(username='TesterTwo', password='SecretCode14!')
        response = self.client.get(
            f'/profile/order_history/{order.order_number}'
            )
        self.assertEqual(response.context['user'], order.user_profile.user)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout_success.html')

    def test_404_raised_for_logged_in_user_but_user_profile_not_on_order(self):
        """
        Login the user who is not attached to the order and check they cannot
        access the page using that order number. Check the response is 404.
        """
        order = Order.objects.get(id=1)
        self.client.login(username='Tester', password='SecretCode14')
        response = self.client.get(
            f'/profile/order_history/{order.order_number}'
            )
        self.assertNotEqual(response.context['user'], order.user_profile.user)
        self.assertEqual(response.status_code, 404)


class TestUpdateSavedMarketsView(TestCase):
    """Tests for update_saved_markets_list view"""
    @classmethod
    def setUpTestData(cls):
        """
        Test user and Market instances so can test adding
        a market to the saved list.
        """
        user1 = User.objects.create_user(
            username='Tester',
            password='SecretCode14',
        )
        user1.save()

        County.objects.create(
            name='dublin_3',
            friendly_name='Dublin 3'
        )
        Market.objects.create(
            name='The Craft Market',
            county=County.objects.get(id=1),
            location='The Street',
            date=datetime.date.today(),
            start_time='09:00',
            end_time='17:00',
            website='http://www.crafted.ie',
        )
        Market.objects.create(
            name='The Other Market',
            county=County.objects.get(id=1),
            location='The Field',
            date=datetime.date.today(),
            start_time='10:00',
            end_time='16:00',
            website='http://www.other.ie',
        )

    def test_405_raised_for_get_request(self):
        """
        View restricted to post requests.
        Test 405 (method not allowed) is raised for a get request.
        """
        self.client.login(username='Tester', password='SecretCode14')
        response = self.client.get('/profile/update_my_markets/1')
        self.assertEqual(response.status_code, 405)

    def test_logged_in_user_can_save_their_first_market(self):
        """
        Login the user, save a market. Get the user's profile and the market
        that was saved, and their saved markets list. Confirm that the market
        just saved is on the list for that user.
        """
        self.client.login(username='Tester', password='SecretCode14')
        response = self.client.post('/profile/update_my_markets/1', {
            'market_id': '1',
            'redirect_url': '/markets/'
        })
        self.assertRedirects(response, '/markets/')
        market = Market.objects.get(id=1)
        user_profile = UserProfile.objects.get(id=1)
        saved_market_list = SavedMarketList.objects.get(user=user_profile)
        self.assertTrue(market in saved_market_list.market.all())

    def test_logged_in_user_can_save_another_market_to_list(self):
        """
        Login the user, save a market (which creates the saved list), then
        add another market. Confirm that both of the markets are in the
        saved markets list for that user.
        """
        self.client.login(username='Tester', password='SecretCode14')
        response = self.client.post('/profile/update_my_markets/1', {
            'market_id': '1',
            'redirect_url': '/markets/'
        })
        response = self.client.post('/profile/update_my_markets/2', {
            'market_id': '2',
            'redirect_url': '/markets/'
        })
        self.assertRedirects(response, '/markets/')
        market1 = Market.objects.get(id=1)
        market2 = Market.objects.get(id=2)
        user_profile = UserProfile.objects.get(id=1)
        saved_market_list = SavedMarketList.objects.get(user=user_profile)
        self.assertTrue(market1 in saved_market_list.market.all())
        self.assertTrue(market2 in saved_market_list.market.all())

    def test_success_message_displayed_when_market_saved(self):
        """
        Login the user, save a market. Check success message generates
        and wording is correct.
        """
        self.client.login(username='Tester', password='SecretCode14')
        response = self.client.post('/profile/update_my_markets/1', {
            'market_id': '1',
            'redirect_url': '/markets/'
        })
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, 'success')
        expected_date = datetime.date.today()
        formatted_date = expected_date.strftime('%d/%m/%Y')
        self.assertEqual(
            messages[0].message,
            f'Market: "The Craft Market on {formatted_date}" added to your '
            'saved markets!'
            )

    def test_logged_in_user_can_remove_a_market_and_list_remains(self):
        """
        Login the user, create their market list and add two market.
        Post request to remove one market. Confirm redirects, confirm the
        saved market list still exists but removed market no longer on the list
        """
        user_profile = UserProfile.objects.get(id=1)
        saved_market_list = SavedMarketList.objects.create(
            user=user_profile
            )
        markets = Market.objects.all()
        for market in markets:
            saved_market_list.market.add(market)
        self.client.login(username='Tester', password='SecretCode14')
        response = self.client.post('/profile/update_my_markets/1', {
            'market_id': '1',
            'redirect_url': '/markets/'
        })
        self.assertRedirects(response, '/markets/')
        saved_market_list = SavedMarketList.objects.get(user=user_profile)
        self.assertFalse(markets[0] in saved_market_list.market.all())
        self.assertTrue(markets[1] in saved_market_list.market.all())

    def test_logged_in_user_can_remove_a_market_and_list_is_deleted(self):
        """
        Login the user, create their market list and add a market.
        Post request to remove the market. Confirm redirects, confirm the
        saved market list no longer exists (deleted as no markets left on it)
        """
        user_profile = UserProfile.objects.get(id=1)
        saved_market_list = SavedMarketList.objects.create(
            user=user_profile
            )
        market = Market.objects.get(id=1)
        saved_market_list.market.add(market)
        self.client.login(username='Tester', password='SecretCode14')
        response = self.client.post('/profile/update_my_markets/1', {
            'market_id': '1',
            'redirect_url': '/markets/'
        })
        self.assertRedirects(response, '/markets/')
        self.assertTrue(saved_market_list.DoesNotExist())


class TestShowSavedMarketsView(TestCase):
    """Tests for show_saved_markets view"""
    @classmethod
    def setUpTestData(cls):
        """
        Test user and 10 Market instances. Instance of SavedMarketList, add
        7 markets to it (mix of dates in future + past).
        Test instances of county for creating markets with different counties
        for filtering by county test.
        """
        user1 = User.objects.create_user(
            username='Tester',
            password='SecretCode14',
        )
        user1.save()
        county_1 = County.objects.create(
            name='dublin_3',
            friendly_name='Dublin 3'
        )
        county_2 = County.objects.create(
            name='dublin_4',
            friendly_name='Dublin 3'
        )
        today = datetime.date.today()
        for market in range(10):
            increment = today + datetime.timedelta(days=market)
            decrement = today - datetime.timedelta(days=market)
            Market.objects.create(
                name='The Craft Market',
                county=county_1 if market % 2 else county_2,
                location='The Street',
                date=increment if market % 2 else decrement,
                start_time='09:00',
                end_time='17:00',
                website='http://www.crafted.ie',
            )
        saved_market_list = SavedMarketList.objects.create(
            user=UserProfile.objects.get(id=1)
            )
        for market in Market.objects.filter(id__lt=8):
            saved_market_list.market.add(market)

    def test_redirects_if_not_logged_in(self):
        """
        View restricted to logged in users. Test user redirected to login
        page if not logged in, with redirect to add market page after login.
        """
        response = self.client.get('/profile/my_markets/')
        self.assertRedirects(
            response, '/accounts/login/?next=/profile/my_markets/'
            )

    def test_correct_url_and_template_used_for_logged_in_user(self):
        """
        Get url for my markets page, check response is 200 + correct template
        """
        self.client.login(username='Tester', password='SecretCode14')
        response = self.client.get('/profile/my_markets/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/my_markets.html')

    def test_all_markets_from_saved_list_displayed(self):
        """
        Check view returns 7 markets i.e. those that were added to the saved
        market list instance, including those in the past.
        """
        self.client.login(username='Tester', password='SecretCode14')
        response = self.client.get('/profile/my_markets/')
        self.assertTrue('markets' in response.context)
        self.assertEqual(len(response.context['markets']), 7)

    def test_sort_request_urls_and_context_are_correct(self):
        """
        For sort requests, check that each combination of url is successful
        And that the 'current_sorting' returned in context is correct
        """
        self.client.login(username='Tester', password='SecretCode14')
        response = self.client.get('/profile/my_markets/')
        self.assertEqual(response.context['current_sorting'], 'None_None')
        sort_options = ['name', 'date']
        for opt in sort_options:
            response = self.client.get(
                f'/profile/my_markets/?sort={opt}&direction=desc'
                )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.context['current_sorting'], f'{opt}_desc'
                )
        for opt in sort_options:
            response = self.client.get(
                f'/profile/my_markets/?sort={opt}&direction=asc'
                )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context['current_sorting'], f'{opt}_asc')

    def test_sort_by_name_returns_markets_in_correct_order(self):
        """
        Test order of markets returned for a sort by name request is correct,
        by checking 1st and last. Markets created with A + Z and names, and
        added to user's saved market list to test
        """
        user_profile = UserProfile.objects.get(id=1)
        saved_market_list = SavedMarketList.objects.get(
            user=user_profile
            )
        names = ['A First Market', 'Z Last Market']
        for market in range(2):
            new_market = Market.objects.create(
                    name=names[market],
                    county=County.objects.get(id=1),
                    location='The Street',
                    date=datetime.date.today(),
                    start_time='09:00',
                    end_time='17:00',
                    website='http://www.aacrafted.ie',
                )
            saved_market_list.market.add(new_market)

        self.client.login(username='Tester', password='SecretCode14')
        # sort ascending name
        response = self.client.get(
            '/profile/my_markets/?sort=name&direction=asc'
            )
        self.assertEqual(
            response.context['markets'][0].name, 'A First Market'
            )
        # have to use len minus 1 here, as negative indexing not supported
        last_item = len(response.context['markets'])-1
        self.assertEqual(
            response.context['markets'][last_item].name, 'Z Last Market'
            )
        # sort descending name
        response = self.client.get(
            '/profile/my_markets/?sort=name&direction=desc'
            )
        self.assertEqual(
            response.context['markets'][0].name,
            'Z Last Market'
            )
        last_item = len(response.context['markets'])-1
        self.assertEqual(
            response.context['markets'][last_item].name, 'A First Market'
            )

    def test_sort_by_date_returns_markets_in_correct_order(self):
        """
        Test that order of markets returned for a sort by date request is
        correct by checking 1st and last. Earliest date is the earlies market
        created in setUp, since past dates are show in this view
        """
        today = datetime.date.today()
        earliest_date = today - datetime.timedelta(days=6)
        latest_date = today + datetime.timedelta(days=5)
        self.client.login(username='Tester', password='SecretCode14')
        # sort ascending date
        response = self.client.get(
            '/profile/my_markets/?sort=date&direction=asc'
            )
        self.assertEqual(
            response.context['markets'][0].date, earliest_date
            )
        last_item = len(response.context['markets'])-1
        self.assertEqual(
            response.context['markets'][last_item].date, latest_date
            )
        # sort descending date
        response = self.client.get(
            '/profile/my_markets/?sort=date&direction=desc'
            )
        self.assertEqual(
            response.context['markets'][0].date, latest_date
            )
        last_item = len(response.context['markets'])-1
        self.assertEqual(
            response.context['markets'][last_item].date, earliest_date
            )

    def test_county_filtering_returns_correct_markets(self):
        """
        If county is selected, ensure only markets in that county shown.
        Check that markets page initially contains 7 saved markets.
        Filter using to county1 name, check 3 markets returned
        Filter using to county2 name, check 4 markets returned
        """
        self.client.login(username='Tester', password='SecretCode14')
        response = self.client.get('/profile/my_markets/')
        self.assertEqual(len(response.context['markets']), 7)
        response = self.client.get('/profile/my_markets/?county=dublin_3')
        self.assertEqual(len(response.context['markets']), 3)
        for market in response.context['markets']:
            self.assertEqual(market.county.name, 'dublin_3')
        response = self.client.get('/profile/my_markets/?county=dublin_4')
        self.assertEqual(len(response.context['markets']), 4)
        for market in response.context['markets']:
            self.assertEqual(market.county.name, 'dublin_4')
