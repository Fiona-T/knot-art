"""Tests for views in 'home' app"""
from django.test import TestCase


class TestViews(TestCase):
    """To test the views for 'home' app which displays static home page"""
    def test_home_page_view(self):
        """
        get the url for home page, check the response is 200 (i.e. successful)
        check the correct template is used - index.html in home app
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')
