"""Tests for models in profiles app"""
import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from markets.models import Market, County
from .models import UserProfile, SavedMarketList


class TestUserProfileModel(TestCase):
    """Tests for UserProfile model"""
    def test_instance_created_and_string_method_returns_username(self):
        """
        Create instance of User, which automatically creates instance of
        UserProfile. Get the user profile instance.
        Call string method on user profile to ensure username returned.
        """
        user = User.objects.create(
            username='Tester',
            password='SecretCode14',
        )
        user.save()
        profile = UserProfile.objects.get(id=1)
        self.assertEqual(str(profile), 'Tester')


class TestSavedMarketListModel(TestCase):
    """Tests for SavedMarketList model"""
    def test_string_method_returns_correct_string(self):
        """
        Create a user, which creates a UserProfile instance, create a
        market. Create instance of SavedMarketList using profile. Add the
        market to it. Confirm string method returns correct string.
        """
        user = User.objects.create(
            username='Tester',
            password='SecretCode14',
        )
        user.save()
        profile = UserProfile.objects.get(id=1)
        county = County.objects.create(
            name='dublin_4',
            friendly_name='Dublin 4'
        )
        market = Market.objects.create(
            name='The Craft Market',
            county=county,
            location='The Street',
            date=datetime.date.today(),
            start_time='09:00',
            end_time='17:00',
            website='www.crafted.ie',
        )
        saved_market_list = SavedMarketList.objects.create(
            user=profile,
        )
        saved_market_list.save()
        saved_market_list.market.add(market)
        self.assertEqual(str(saved_market_list), 'Tester\'s saved markets')
