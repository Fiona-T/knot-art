"""Tests for views in 'markets' app"""
import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from .models import County, Market


class TestShowMarketsView(TestCase):
    """To test the show_markets view - page displaying markets"""
    @classmethod
    def setUp(cls):
        """
        Create instance of County
        Create 7 instances of Market, one today's date, 3 each before
        and after this date - for tests depending on market date.
        """
        County.objects.create(
            name='dublin_3',
            friendly_name='Dublin 3'
        )
        today = datetime.date.today()
        for market in range(7):
            increment = today + datetime.timedelta(days=market)
            decrement = today - datetime.timedelta(days=market)
            Market.objects.create(
                name='The Craft Market',
                location='The Street',
                county=County.objects.get(id=1),
                date=increment if market % 2 else decrement,
                start_time='09:00',
                end_time='17:00',
                website='www.crafted.ie',
            )

    def test_correct_url_and_template_used(self):
        """
        Get url for markets page, check response is 200 + correct template
        """
        response = self.client.get('/markets/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'markets/markets.html')

    def test_only_markets_dated_today_or_after_are_displayed(self):
        """
        Check view returns 4 markets i.e. from those created in setUp dated
        today or in future. Confirm date greater/equal to today.
        """
        response = self.client.get('/markets/')
        self.assertTrue('markets' in response.context)
        self.assertEqual(len(response.context['markets']), 4)
        for market in response.context['markets']:
            self.assertGreaterEqual(market.date, datetime.date.today())

    def test_soonest_market_shown_first_for_non_superuser(self):
        """
        Test ordering for non-superuser. If no order selected, the soonest
        should be displayed first + dated today. And latest last.
        """
        response = self.client.get('/markets/')
        today = datetime.date.today()
        latest = today + datetime.timedelta(days=5)
        self.assertEqual(response.context['markets'][0].date, today)
        self.assertEqual(response.context['markets'][3].date, latest)

    def test_all_markets_displayed_for_superuser(self):
        """
        Create a superuser, log them in. Check view returns 7 markets i.e. all
        including those in the past.
        """
        test_superuser = User.objects.create_user(
            username='admin',
            password='secret',
            is_superuser=True
        )
        test_superuser.save()

        self.client.login(username='admin', password='secret')
        response = self.client.get('/markets/')
        self.assertTrue('markets' in response.context)
        self.assertEqual(len(response.context['markets']), 7)


class TestAddMarketView(TestCase):
    """Tests for add_market view"""
    @classmethod
    def setUpTestData(cls):
        """
        Standard user and Superuser for access tests.
        County and Market instance for tests.
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

        County.objects.create(
            name='dublin_3',
            friendly_name='Dublin 3'
        )
        today = datetime.date.today()
        Market.objects.create(
            name='The Craft Market',
            location='The Street',
            county=County.objects.get(id=1),
            date=today + datetime.timedelta(days=5),
            start_time='09:00',
            end_time='17:00',
            website='www.crafted.ie',
        )

    def test_redirects_if_not_logged_in(self):
        """
        View restricted to logged in users. Test user redirected to login
        page if not logged in, with redirect to add market page after login.
        """
        response = self.client.get('/markets/add/')
        self.assertRedirects(response, '/accounts/login/?next=/markets/add/')

    def test_403_raised_if_logged_in_but_not_superuser(self):
        """
        View restricted to logged in superusers. Test logged in user who is
        not a superuser gets a 403 response (permission denied)
        """
        self.client.login(username='User', password='secret12')
        response = self.client.get('/markets/add/')
        self.assertEqual(response.status_code, 403)

    def test_correct_url_and_template_used_for_logged_in_superuser(self):
        """Get the url, check response is 200 + correct template"""
        self.client.login(username='admin', password='secret')
        response = self.client.get('/markets/add/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'markets/add_market.html')

    def test_can_add_market(self):
        """
        login the admin user, get markets url and check length of markets is
        one initially (existing market). Then do POST request on add market
        url, with test market. Check redirects to the correct success url
        after adding. Check that length of markets is now 2, and name matches.
        """
        self.client.login(username='admin', password='secret')
        response = self.client.get('/markets/')
        self.assertEqual(len(response.context['markets']), 1)
        today = datetime.date.today()
        response = self.client.post('/markets/add/', {
            'name': 'The New Market',
            'location': 'The Lane',
            'county': 1,
            'date': today + datetime.timedelta(days=1),
            'start_time': '09:30',
            'end_time': '17:30',
            'website': 'http://www.new.ie',
        })
        self.assertRedirects(response, '/markets/')
        response = self.client.get('/markets/')
        self.assertEqual(len(response.context['markets']), 2)
        self.assertEqual(
            response.context['markets'][1].name, 'The New Market'
            )

    def test_success_message_displayed_when_market_added(self):
        """Add a market and check msg displayed + is correct"""
        self.client.login(username='admin', password='secret')
        today = datetime.date.today()
        response = self.client.post('/markets/add/', {
            'name': 'The New Market',
            'location': 'The Lane',
            'county': 1,
            'date': today + datetime.timedelta(days=1),
            'start_time': '09:30',
            'end_time': '17:30',
            'website': 'http://www.new.ie',
        })
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, 'success')
        expected_date = today + datetime.timedelta(days=1)
        formatted_date = expected_date.strftime('%d/%m/%Y')
        self.assertEqual(
            messages[0].message,
            f'New market: "The New Market" on {formatted_date} added!'
            )

    def test_error_message_displayed_when_form_not_valid(self):
        """
        Attempt to add market with invalid form, confirm form is invalid,
        check error msg is displayed + is correct.
        """
        self.client.login(username='admin', password='secret')
        today = datetime.date.today()
        response = self.client.post('/markets/add/', {
            'name': 'The New Market',
            'location': 'The Lane',
            'county': 1,
            'date': today - datetime.timedelta(days=1),  # invalid
            'start_time': '09:30',
            'end_time': '17:30',
            'website': 'http://www.new.ie',
        })
        self.assertFalse(response.context['form'].is_valid())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, 'error')
        self.assertEqual(
            messages[0].message,
            'Market not added. Please check the form for errors and '
            're-submit.'
            )
