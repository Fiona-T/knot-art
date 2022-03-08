"""models for products app"""
from django.db import models


class Category(models.Model):
    """Category model for products"""

    class Meta:
        """Specify correct spelling for plural - for admin site"""
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=50, unique=True)
    friendly_name = models.CharField(max_length=50)

    def __str__(self):
        """string method - return the category name"""
        return self.name

    def get_friendly_name(self):
        """return the user friendly name - for views"""
        return self.friendly_name


class Product(models.Model):
    """Product model - for products in shop"""

    category = models.ForeignKey(
        'Category',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='products_in_category'
        )
    sku = models.CharField(max_length=50)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_new = models.BooleanField(default=True)

    def __str__(self):
        """string method - return the product name and category"""
        return f'{self.name} in {self.category}'
