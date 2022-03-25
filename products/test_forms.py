"""Tests for forms in products app - shop"""
from django.test import TestCase
from .forms import ProductForm


class TestProductForm(TestCase):
    """Tests for the ProductForm"""
    def test_explicitly_set_field_labels_exist(self):
        """
        Check labels are present for the fields where a label was explicitly
        set in the form Meta class
        """
        form = ProductForm()
        self.assertTrue(
            form.fields['is_active'].label is None or
            form.fields['is_active'].label == 'Active product?'
            )
        self.assertTrue(
            form.fields['is_new'].label is None or
            form.fields['is_new'].label == 'New product?'
            )

    def test_helptext_exists_and_correct_where_set_in_meta_class(self):
        """
        Test helptext present and correct on fields that should have it
        """
        form = ProductForm()
        help_texts = {
            'name': 'Product name must be unique',
            'is_active': 'Only active products are visible in the shop to '
            'users. Leave un-checked if product not ready to be shown in shop',
            'is_new': 'A "New!" badge will be shown on the product if this '
            'is ticked',
            }
        for field in form.fields:
            if field in help_texts.keys():
                self.assertEqual(
                    form.fields[field].help_text, help_texts[field])

    def test_css_class_exists_on_fields(self):
        """Test CSS class is present and correct on the form fields"""
        form = ProductForm()
        for field in form.fields:
            self.assertEqual(
                form.fields[field].widget.attrs['class'], 'order-form-input')

    def test_required_fields_are_required(self):
        """
        Check form is not valid if required fields are blank.
        Test required fields are in form errors, not required not.
        Check error message exists for each required field.
        """
        form = ProductForm({
            'category': '',
            'sku': '',
            'name': '',
            'description': '',
            'price': '',
            'image_url': '',
            'image': '',
            'is_active': '',
            'is_new': '',
        })

        required_fields = [
            'sku',
            'name',
            'description',
            'price',
            ]
        for field in required_fields:
            self.assertIn(field, form.errors.keys())
            self.assertEqual(form.errors[field][0], 'This field is required.')

        not_required_fields = [
            'category', 'image_url', 'image', 'is_active', 'is_new',
            ]
        for field in not_required_fields:
            self.assertNotIn(field, form.errors.keys())