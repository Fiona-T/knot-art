"""Tests for views in 'markets' app"""
import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from .models import County, Market, Comment


class TestShowMarketsView(TestCase):
    """To test the show_markets view - page displaying markets"""
    @classmethod
    def setUp(cls):
        """
        Create 2 instances of County
        Create 7 instances of Market, one today's date, 3 each before
        and after this date - for tests depending on market date.
        Create 5 instances of market, 2 with 1st county, 3 with 2nd county,
        for tests of filtering by county
        """
        county_1 = County.objects.create(
            name='dublin_3',
            friendly_name='Dublin 3'
        )
        county_2 = County.objects.create(
            name='dublin_4',
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
                website='http://www.crafted.ie',
            )
        for market in range(5):
            Market.objects.create(
                name='The Craft Market',
                location='The Street',
                county=county_1 if market % 2 else county_2,
                date=today,
                start_time='09:00',
                end_time='17:00',
                website='http://www.crafted.ie',
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
        Check view returns 9 markets i.e. from those created in setUp dated
        today or in future 4 + 5. Confirm date greater/equal to today.
        """
        response = self.client.get('/markets/')
        self.assertTrue('markets' in response.context)
        self.assertEqual(len(response.context['markets']), 9)
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
        self.assertEqual(response.context['markets'][8].date, latest)

    def test_all_markets_displayed_for_superuser(self):
        """
        Create a superuser, log them in. Check view returns 12 markets i.e. all
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
        self.assertEqual(len(response.context['markets']), 12)

    def test_sort_request_urls_and_context_are_correct(self):
        """
        For sort requests, check that each combination of url is successful
        And that the 'current_sorting' returned in context is correct
        """
        response = self.client.get('/markets/')
        self.assertEqual(response.context['current_sorting'], 'None_None')
        sort_options = ['name', 'date']
        for opt in sort_options:
            response = self.client.get(f'/markets/?sort={opt}&direction=desc')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.context['current_sorting'], f'{opt}_desc'
                )
        for opt in sort_options:
            response = self.client.get(f'/markets/?sort={opt}&direction=asc')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context['current_sorting'], f'{opt}_asc')

    def test_sort_by_name_returns_markets_in_correct_order(self):
        """
        Test order of markets returned for a sort by name request is correct,
        by checking 1st and last. Markets created with A + Z and names to test
        """
        names = ['A First Market', 'Z Last Market']
        for market in range(2):
            Market.objects.create(
                    name=names[market],
                    location='The Street',
                    date=datetime.date.today(),
                    start_time='09:00',
                    end_time='17:00',
                    website='http://www.aacrafted.ie',
                )

        response = self.client.get('/markets/?sort=name&direction=asc')
        self.assertEqual(
            response.context['markets'][0].name, 'A First Market'
            )
        # have to use len minus 1 here, as negative indexing not supported
        last_item = len(response.context['markets'])-1
        self.assertEqual(
            response.context['markets'][last_item].name, 'Z Last Market'
            )

        response = self.client.get('/markets/?sort=name&direction=desc')
        self.assertEqual(response.context['markets'][0].name, 'Z Last Market')
        last_item = len(response.context['markets'])-1
        self.assertEqual(
            response.context['markets'][last_item].name, 'A First Market'
            )

    def test_sort_by_date_returns_markets_in_correct_order(self):
        """
        Test that order of markets returned for a sort by date request is
        correct by checking 1st and last. Earliest date from markets in
        setUp will be today because other dates are in past so not shown.
        """
        today = datetime.date.today()
        latest_date = today + datetime.timedelta(days=5)

        response = self.client.get('/markets/?sort=date&direction=asc')
        self.assertEqual(response.context['markets'][0].date, today)
        last_item = len(response.context['markets'])-1
        self.assertEqual(
            response.context['markets'][last_item].date, latest_date
            )
        response = self.client.get('/markets/?sort=date&direction=desc')
        self.assertEqual(response.context['markets'][0].date, latest_date)
        last_item = len(response.context['markets'])-1
        self.assertEqual(
            response.context['markets'][last_item].date, today
            )

    def test_county_filtering_returns_correct_markets(self):
        """
        If county is selected, ensure only markets in that county shown.
        Check that markets page initially contains 9 markets (i.e. those
        dated today or later).
        Filter using to county1 name, check 6 markets returned
        Filter using to county2 name, check 3 markets returned
        """
        response = self.client.get('/markets/')
        self.assertEqual(len(response.context['markets']), 9)
        response = self.client.get('/markets/?county=dublin_3')
        self.assertEqual(len(response.context['markets']), 6)
        for market in response.context['markets']:
            self.assertEqual(market.county.name, 'dublin_3')
        response = self.client.get('/markets/?county=dublin_4')
        self.assertEqual(len(response.context['markets']), 3)
        for market in response.context['markets']:
            self.assertEqual(market.county.name, 'dublin_4')


class TestMarketDetailsView(TestCase):
    """Tests for market_details view to show comments"""
    @classmethod
    def setUp(cls):
        """
        Create instance of County and Market. Create user to create
        Comments on the market for tests.
        """
        County.objects.create(
            name='dublin_3',
            friendly_name='Dublin 3'
        )

        today = datetime.date.today()
        Market.objects.create(
            name='The Craft Market',
            location='The Street',
            county=County.objects.get(id=1),
            date=today,
            start_time='09:00',
            end_time='17:00',
            website='http://www.crafted.ie',
        )
        Market.objects.create(
            name='Market with comments',
            location='The Road',
            county=County.objects.get(id=1),
            date=today,
            start_time='09:00',
            end_time='17:00',
            website='http://www.market.ie',
        )
        test_user = User.objects.create_user(
            username='User',
            password='secret12',
        )
        test_user.save()

        Comment.objects.create(
            author=test_user,
            market=Market.objects.get(id=2),
            comment='This is a comment'
        )
        Comment.objects.create(
            author=test_user,
            market=Market.objects.get(id=2),
            comment='This is a second comment'
        )

    def test_correct_url_and_template_used(self):
        """Get the url, check response is 200 + correct template"""
        response = self.client.get('/markets/1/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'markets/market_details.html')

    def test_comments_are_in_conetxt_when_market_has_comments(self):
        """
        The second market created in setup has 2 comments attached, go to
        page for this market and confirm 2 comments in context.
        """
        response = self.client.get('/markets/2/')
        self.assertTrue('comments' in response.context)
        self.assertEqual(len(response.context['comments']), 2)

    def test_message_displayed_when_there_are_no_comment(self):
        """Check there are no comments shown for market with no comments"""
        response = self.client.get('/markets/1/')
        self.assertEqual(len(response.context['comments']), 0)


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
            f'New market: "The New Market on {formatted_date}" added!'
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


class TestEditMarketView(TestCase):
    """Tests for edit_market view"""
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
        Market.objects.create(
            name='The Old Market',
            location='The Street',
            county=County.objects.get(id=1),
            date='2022-04-10',  # past date
            start_time='09:00',
            end_time='17:00',
            website='http://www.market.ie',
        )

    def test_redirects_if_not_logged_in(self):
        """
        View restricted to logged in users. Test user redirected to login
        page if not logged in, with redirect to add market page after login.
        """
        response = self.client.get('/markets/edit/1/')
        self.assertRedirects(
            response, '/accounts/login/?next=/markets/edit/1/'
            )

    def test_403_raised_if_logged_in_but_not_superuser(self):
        """
        View restricted to logged in superusers. Test logged in user who is
        not a superuser gets a 403 response (permission denied)
        """
        self.client.login(username='User', password='secret12')
        response = self.client.get('/markets/edit/1/')
        self.assertEqual(response.status_code, 403)

    def test_correct_url_and_template_used_for_logged_in_superuser(self):
        """Get the url, check response is 200 + correct template"""
        self.client.login(username='admin', password='secret')
        response = self.client.get('/markets/edit/1/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'markets/edit_market.html')

    def test_can_edit_market(self):
        """
        login the admin user do POST request on edit market url to amend
        details. Check redirects to the correct success url
        Check market in get request has the updated details.
        """
        self.client.login(username='admin', password='secret')
        today = datetime.date.today()
        response = self.client.post('/markets/edit/1/', {
            'name': 'The Edited Craft Market',
            'location': 'The Street Edited',
            'county': 1,
            'date': today + datetime.timedelta(days=5),
            'start_time': '09:00',
            'end_time': '17:00',
            'website': 'www.crafted-edited.ie',
        })
        self.assertRedirects(response, '/markets/')
        response = self.client.get('/markets/')
        updated_market = Market.objects.get(id=1)
        self.assertEqual(updated_market.name, 'The Edited Craft Market')
        self.assertEqual(
            updated_market.location, 'The Street Edited'
            )
        self.assertEqual(
            updated_market.website, 'http://www.crafted-edited.ie'
            )

    def test_success_message_displayed_when_market_edited(self):
        """Edit a market and check msg displayed + is correct"""
        self.client.login(username='admin', password='secret')
        today = datetime.date.today()
        response = self.client.post('/markets/edit/1/', {
            'name': 'The Edited Craft Market',
            'location': 'The Street Edited',
            'county': 1,
            'date': today + datetime.timedelta(days=3),
            'start_time': '09:00',
            'end_time': '17:00',
            'website': 'www.crafted-edited.ie',
        })
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, 'success')
        expected_date = today + datetime.timedelta(days=3)
        formatted_date = expected_date.strftime('%d/%m/%Y')
        self.assertEqual(
            messages[0].message,
            f'Updates to market: "The Edited Craft Market on '
            f'{formatted_date}" saved!'
            )

    def test_error_message_displayed_when_form_not_valid(self):
        """
        Attempt to add market with invalid form, confirm form is invalid,
        check error msg is displayed + is correct.
        """
        self.client.login(username='admin', password='secret')
        today = datetime.date.today()
        response = self.client.post('/markets/edit/1/', {
            'name': 'The Edited Craft Market',
            'location': 'The Street Edited',
            'county': 1,
            'date': today - datetime.timedelta(days=5),  # invalid
            'start_time': '09:00',
            'end_time': '17:00',
            'website': 'www.crafted-edited.ie',
        })
        self.assertFalse(response.context['form'].is_valid())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, 'error')
        self.assertEqual(
            messages[0].message,
            'Market NOT updated. Please check the form for errors and '
            're-submit.'
            )

    def test_info_message_displayed_when_existing_date_is_in_past(self):
        """
        Go to edit page for market with past date, confirm info message is
        displayed + is correct.
        """
        self.client.login(username='admin', password='secret')
        response = self.client.get('/markets/edit/2/')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, 'info')
        self.assertEqual(
            messages[0].message,
            'You\'re editing a past market. You can update the details but if '
            'you change the date, the new date must be a future date.<br>If '
            'you want to post details of this market on a new date, then '
            'create a new market record using the Add Market form.'
            )

    def test_can_edit_market_when_existing_date_is_in_past(self):
        """
        Edit existing market with past date, leaving the date the same. Confirm
        redirects and updated details were saved.
        """
        self.client.login(username='admin', password='secret')
        response = self.client.post('/markets/edit/2/', {
            'name': 'The Edited Old Market',
            'location': 'Address',
            'county': 1,
            'date': '2022-04-10',  # existing past date,
            'start_time': '09:00',
            'end_time': '17:00',
            'website': 'http://www.market.ie',
        })
        self.assertRedirects(response, '/markets/')
        response = self.client.get('/markets/')
        updated_market = Market.objects.get(id=2)
        self.assertEqual(updated_market.name, 'The Edited Old Market')
        self.assertEqual(
            updated_market.location, 'Address'
            )

    def test_can_edit_market_with_date_in_past_to_future_date(self):
        """
        Edit existing market with past date, changing date to today. Confirm
        redirects and updated details were saved.
        """
        self.client.login(username='admin', password='secret')
        today = datetime.date.today()
        response = self.client.post('/markets/edit/2/', {
            'name': 'The Edited Old Market',
            'location': 'Address',
            'county': 1,
            'date': today,  # change past date to today,
            'start_time': '09:00',
            'end_time': '17:00',
            'website': 'http://www.market.ie',
        })
        self.assertRedirects(response, '/markets/')
        response = self.client.get('/markets/')
        updated_market = Market.objects.get(id=2)
        self.assertEqual(updated_market.date, today)

    def test_cannot_edit_market_with_date_in_past_to_another_past_date(self):
        """
        Edit existing market with past date, changing date to yesterday.
        Confirm form is not valid + error msg displayed.
        """
        self.client.login(username='admin', password='secret')
        today = datetime.date.today()
        response = self.client.post('/markets/edit/2/', {
            'name': 'The Edited Old Market',
            'location': 'Address',
            'county': 1,
            'date': today - datetime.timedelta(days=1),
            'start_time': '09:00',
            'end_time': '17:00',
            'website': 'http://www.market.ie',
        })
        self.assertFalse(response.context['form'].is_valid())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, 'error')
        self.assertEqual(
            messages[0].message,
            'Market NOT updated. Please check the form for errors and '
            're-submit.'
            )


class TestDeleteMarkettView(TestCase):
    """Tests for delete_market view"""
    @classmethod
    def setUpTestData(cls):
        """
        Standard user and Superuser for access tests.
        County, Markets instances for tests.
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
            website='http://www.crafted.ie',
        )
        Market.objects.create(
            name='The Lovely Market',
            location='The Lane',
            county=County.objects.get(id=1),
            date=today + datetime.timedelta(days=6),
            start_time='10:00',
            end_time='20:00',
            website='http://www.lovely.ie',
        )

    def test_405_raised_for_get_request(self):
        """
        View restricted to post requests.
        Test 405 (method not allowed) is raised for a get request.
        """
        self.client.login(username='admin', password='secret')
        response = self.client.get('/markets/delete/1/')
        self.assertEqual(response.status_code, 405)

    def test_403_raised_for_regular_user_post_request(self):
        """
        View restricted to logged in superusers. Test logged in user who is
        not a superuser gets a 403 response (permission denied)
        """
        self.client.login(username='User', password='secret12')
        response = self.client.post('/markets/delete/1/')
        self.assertEqual(response.status_code, 403)

    def test_admin_user_can_delete_market(self):
        """
        Confirm logged in admin user can delete market, the page
        refirects to the correct page, the number of markets on the
        markets page is reduced by 1.
        """
        self.client.login(username='admin', password='secret')
        response = self.client.get('/markets/')
        self.assertEqual(len(response.context['markets']), 2)
        response = self.client.post('/markets/delete/1/')
        self.assertRedirects(response, '/markets/')
        response = self.client.get('/markets/')
        self.assertEqual(len(response.context['markets']), 1)

    def test_success_message_displayed_when_market_deleted(self):
        """Delete a market and check msg displayed + is correct"""
        self.client.login(username='admin', password='secret')
        response = self.client.post('/markets/delete/1/')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, 'success')
        expected_date = datetime.date.today() + datetime.timedelta(days=5)
        formatted_date = expected_date.strftime('%d/%m/%Y')
        self.assertEqual(
            messages[0].message,
            f'Market: "The Craft Market on { formatted_date }" deleted!'
            )
