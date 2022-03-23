"""Tests for views in profiles app"""
from django.test import TestCase
from django.contrib.auth.models import User


class TestProfileView(TestCase):
    """Tests for profile view"""
    @classmethod
    def setUpTestData(cls):
        """ Create a test user """
        user = User.objects.create_user(
            username='Tester',
            password='SecretCode14',
        )
        user.save()

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
