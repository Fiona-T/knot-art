"""Tests for views in 'markets' app"""
import datetime
from django.test import TestCase
from django.contrib.auth.models import User
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
