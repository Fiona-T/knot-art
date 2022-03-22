"""Tests for views in profiles app"""
from django.test import TestCase


class TestProfileView(TestCase):
    """Tests for profile view"""
    def test_correct_url_and_template_used(self):
        """
        get url for profile page, check the response is 200 (i.e. successful),
        check the correct template is used - profile.html in profiles app
        Note: will need to be updated with login etc. once view developed more
        """
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')
