"""Tests for forms in profiles app"""
from django.test import TestCase
from .forms import UserProfileForm


class TestUserProfileForm(TestCase):
    """Tests for the UserProfileForm"""
    def test_explicitly_set_field_labels_exist(self):
        """
        Check labels are present for the fields where a label was explicitly
        set in the form Meta class
        """
        form = UserProfileForm()
        self.assertTrue(
            form.fields['default_street_address1'].label is None or
            form.fields[
                'default_street_address1'].label == 'Default Street address 1'
            )
        self.assertTrue(
            form.fields['default_street_address2'].label is None or
            form.fields[
                'default_street_address2'].label == 'Default Street address 2'
            )

    def test_placeholders_exist(self):
        """
        Test placeholders present and correct on fields that should have them
        """
        form = UserProfileForm()
        placeholders = {
            'default_postcode': 'Postal Code or Eircode',
            'default_county': 'County, State or Locality',
        }
        for field in form.fields:
            if field in placeholders.keys():
                self.assertEqual(
                    form.fields[field].widget.attrs['placeholder'],
                    placeholders[field]
                    )

    def test_css_class_exists_on_fields(self):
        """Test CSS class is present and correct on the form fields"""
        form = UserProfileForm()
        for field in form.fields:
            if field == 'default_country':
                self.assertEqual(
                    form.fields[field].widget.attrs['class'],
                    'brand-form-input country-input'
                    )
            else:
                self.assertEqual(
                    form.fields[field].widget.attrs['class'],
                    'brand-form-input'
                    )
