"""Unit tests for Models in 'markets' app"""
import datetime
from django.test import TestCase
from django.db import IntegrityError
from django.contrib.auth.models import User
from .models import County, Market, Comment


class TestCountyModel(TestCase):
    """tests for County model in markets app"""
    @classmethod
    def setUpTestData(cls):
        """Create instance of County model for tests"""
        County.objects.create(
            name='dublin_2',
            friendly_name='Dublin 2'
        )

    def test_countyy_name_must_be_unique_in_table(self):
        """
        Check that creating another record with the same name
        as the instance created in the setUp raises an error
        """
        with self.assertRaises(IntegrityError):
            County.objects.create(
                name='dublin_2',
                friendly_name='A different name',
            )

    def test_get_friendly_name_returns_friendly_name(self):
        """
        Get the record created in setUp, check that the get_friendly_name
        method called on this record returns the friendly_name
        """
        county = County.objects.get(id=1)
        self.assertEqual(county.get_friendly_name(), 'Dublin 2')

    def test_string_method_returns_county_name(self):
        """
        Get the record created in setUp, check that the string method called
        on this record returns the name
        """
        county = County.objects.get(id=1)
        self.assertEqual(str(county), 'dublin_2')

    def test_verbose_name_plural_returns_counties(self):
        """check verbose_name_plural is set, as defined in Meta class"""
        county = County.objects.get(id=1)
        self.assertEqual(county._meta.verbose_name_plural, 'Counties')


class TestMarketModel(TestCase):
    """tests for Market model in markets app"""
    @classmethod
    def setUpTestData(cls):
        """
        Create instance of County for creating Market instances.
        Create 3 instances of Market: 1 with specific date, 1 dated today,
        1 dated yesterday so can test date_passed property.
        """
        County.objects.create(
            name='dublin_2',
            friendly_name='Dublin 2'
        )

        today = datetime.date.today()

        Market.objects.create(
            name='The Craft Market',
            location='The Street',
            county=County.objects.get(id=1),
            date=today + datetime.timedelta(days=3),
            start_time='09:00',
            end_time='17:00',
            website='www.crafted.ie',
        )
        Market.objects.create(
            name='The Craft Market',
            location='The Street',
            county=County.objects.get(id=1),
            date=today,
            start_time='09:00',
            end_time='17:00',
            website='www.crafted.ie',
        )
        Market.objects.create(
            name='The Craft Market',
            location='The Street',
            county=County.objects.get(id=1),
            date=today - datetime.timedelta(days=1),
            start_time='09:00',
            end_time='17:00',
            website='www.crafted.ie',
        )

    def test_string_method_returns_market_name_and_date(self):
        """
        Get the market record created in setUp. Check that the string method
        called on this record returns the correct string
        """
        market = Market.objects.get(id=1)
        today = datetime.date.today()
        expected_date = today + datetime.timedelta(days=3)
        formatted_date = expected_date.strftime('%d/%m/%Y')
        self.assertEqual(str(market), f'The Craft Market on {formatted_date}')

    def test_date_passed_property_returns_true_if_date_passed(self):
        """Market id 3 has date of yesterday, confirm date_passed is true"""
        market = Market.objects.get(id=3)
        self.assertTrue(market.date_passed)

    def test_date_passed_property_returns_false_if_date_not_passed(self):
        """Market id 2 has date of today, confirm date_passed is false"""
        market = Market.objects.get(id=2)
        self.assertFalse(market.date_passed)


class TestCommentModel(TestCase):
    """tests for Comment model in markets app"""
    @classmethod
    def setUpTestData(cls):
        """
        Create instance of County for creating Market instances.
        Create instance of Market and Comment linked to that market,
        create User to link to the comment.
        """
        County.objects.create(
            name='dublin_2',
            friendly_name='Dublin 2'
        )
        Market.objects.create(
            name='The Craft Market',
            location='The Street',
            county=County.objects.get(id=1),
            date=datetime.date.today(),
            start_time='09:00',
            end_time='17:00',
            website='http://www.crafted.ie',
        )
        User.objects.create(
            username='Tester',
            password='SecretCode14',
        )
        Comment.objects.create(
            author=User.objects.get(id=1),
            market=Market.objects.get(id=1),
            comment='This is the comment',
        )

    def test_string_method_returns_author_created_on_and_market(self):
        """
        Get the comment instance created in setUp. Check that the string method
        called on this instance returns the correct string.
        """
        comment = Comment.objects.get(id=1)
        expected_market_date = datetime.date.today()
        formatted_date = expected_market_date.strftime('%d/%m/%Y')
        self.assertEqual(
            str(comment),
            f'Comment by Tester, {comment.created_on}, on The Craft Market '
            f'on {formatted_date}'
            )
