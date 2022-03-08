"""Unit tests for Models in 'products' app"""
from django.test import TestCase
from django.db import IntegrityError
from .models import Category, Product


class TestCategoryModel(TestCase):
    """tests for Category model in products app"""
    @classmethod
    def setUpTestData(cls):
        """Create instance of Category model for tests"""
        Category.objects.create(
            name='category_and_category',
            friendly_name='Category & Category'
        )

    def test_category_name_is_unique_in_table(self):
        """
        Check that creating another record with the same name
        as the instance created in the setUp raises an error
        """
        with self.assertRaises(IntegrityError):
            Category.objects.create(
                name='category_and_category',
                friendly_name='A different name',
            )

    def test_get_friendly_name_returns_friendly_name(self):
        """
        Get the record created in setUp, check that the get_friendly_name
        method called on this record returns the friendly_name
        """
        category = Category.objects.get(id=1)
        self.assertEqual(category.get_friendly_name(), 'Category & Category')

    def test_string_method_returns_category_name(self):
        """
        Get the record created in setUp, check that the string method called
        on this record returns the name
        """
        category = Category.objects.get(id=1)
        self.assertEqual(str(category), 'category_and_category')


class TestProductModel(TestCase):
    """tests for Product model in products app"""
    @classmethod
    def setUpTestData(cls):
        """Create instance of Category + Product models for tests"""
        Category.objects.create(
            name='category_and_category',
            friendly_name='Category & Category'
        )

        Product.objects.create(
            category=Category.objects.get(id=1),
            name='product name',
            sku='12345',
            description='product description',
            price=123.45,
            is_active=True,
            is_new=True
        )

    def test_product_name_is_unique_in_table(self):
        """
        Check that creating a product record with the same name raises as
        the one created in setUp raises an error
        """
        with self.assertRaises(IntegrityError):
            Product.objects.create(
                category=Category.objects.get(id=1),
                name='product name',
                sku='1234567',
                description='product description new',
                price=1563.45,
                is_active=False,
                is_new=True
            )

    def test_is_active_flag_defaults_to_true(self):
        """
        Create a product without setting the is_active flag. Check the
        flag defaults to true
        """
        product = Product.objects.create(
            category=Category.objects.get(id=1),
            name='different product name',
            sku='1234567',
            description='product description new',
            price=1563.45,
            is_new=True
            )
        self.assertTrue(product.is_active)

    def test_is_new_flag_defaults_to_true(self):
        """
        Create a product without setting the is_new flag. Check the
        flag defaults to true
        """
        product = Product.objects.create(
            category=Category.objects.get(id=1),
            name='different product name',
            sku='1234567',
            description='product description new',
            price=1563.45,
            is_active=False
            )
        self.assertTrue(product.is_new)

    def test_string_method_returns_product_and_category_name(self):
        """
        Get the product record created in setUp. Check that the string method
        called on this record returns the correct string
        """
        product = Product.objects.get(id=1)
        self.assertEqual(str(product), 'product name in category_and_category')
