"""Tests for models in profiles app"""
from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile


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
