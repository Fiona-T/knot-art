"""Tests for forms in checkout app"""
from django.test import TestCase
from .forms import OrderForm


class TestOrderForm(TestCase):
    """Tests for the OrderForm"""
    def test_fields_are_explicit_in_form_metaclass(self):
        """
        Check the Meta fields attribute is equal to the list of fields
        defined in the form Meta innerclass
        """
        form = OrderForm()
        self.assertEqual(
            form.Meta.fields, (
                'full_name',
                'email',
                'phone_number',
                'street_address1',
                'street_address2',
                'town_or_city',
                'postcode',
                'country',
                'county',
                )
            )

    def test_explicitly_set_field_labels_exist(self):
        """
        Check labels are present for the fields where a label was explicitly
        set in the form Meta class
        """
        form = OrderForm()
        self.assertTrue(
            form.fields['street_address1'].label is None or
            form.fields['street_address1'].label == 'Street address 1'
            )
        self.assertTrue(
            form.fields['street_address2'].label is None or
            form.fields['street_address2'].label == 'Street address 2'
            )

    def test_required_fields_are_required(self):
        """
        Check form is not valid if required fields are blank.
        Test required fields are in form errors, not required not.
        Check error message exists for each required field.
        """
        form = OrderForm({
            'full_name': '',
            'email': '',
            'phone_number': '',
            'street_address1': '',
            'street_address2': '',
            'town_or_city': '',
            'postcode': '',
            'country': '',
            'county': '',
        })

        self.assertFalse(form.is_valid())

        required_fields = [
            'full_name',
            'email',
            'phone_number',
            'street_address1',
            'town_or_city',
            'country',
            ]
        for field in required_fields:
            self.assertIn(field, form.errors.keys())
            self.assertEqual(form.errors[field][0], 'This field is required.')

        not_required_fields = ['street_address2', 'postcode', 'county', ]
        for field in not_required_fields:
            self.assertNotIn(field, form.errors.keys())

    def test_placeholders_exist(self):
        """
        Test placeholders present and correct on fields that should have them
        """
        form = OrderForm()
        placeholders = {
            'email': 'example@example.com',
            'postcode': 'Postal Code or Eircode',
            'county': 'County, State or Locality',
        }
        for field in form.fields:
            if field in placeholders.keys():
                self.assertEqual(
                    form.fields[field].widget.attrs['placeholder'],
                    placeholders[field]
                    )

    def test_css_class_exists_on_fields(self):
        """Test class present and correct on the form fields"""
        form = OrderForm()
        for field in form.fields:
            self.assertEqual(
                form.fields[field].widget.attrs['class'],
                'brand-form-input'
                )
