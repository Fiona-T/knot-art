"""
models for checkout app - handle checkout process. Credit: Code Institute
"""
import uuid
from django.db import models
from django.db.models import Sum
from django.conf import settings
from django_countries.fields import CountryField
from products.models import Product
from profiles.models import UserProfile


class Order(models.Model):
    """
    The order as a whole, with the delivery details.
    Two fields are unique identifiers in webhook handler to check if order
    already exists (so can create if not): original_cart and stripe_pid.
    UserProfile attached so order history can be shown in profile page.
    """
    order_number = models.CharField(max_length=32, null=False, editable=False)
    user_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
        )
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    country = CountryField(
        blank_label='Choose country from dropdown',
        null=False,
        blank=False)
    date = models.DateTimeField(auto_now_add=True)
    order_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0
        )
    delivery_cost = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0
        )
    grand_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0
        )
    original_cart = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(
        max_length=254,
        null=False,
        blank=False,
        default=''
        )

    def _generate_order_number(self):
        """
        Private method to generate random unique string of 32 chars
        using UUID, this will be used as an order number
        """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Sum across line items, calculate delivery costs and get the
        new grand total - each time a line item is added.
        """
        self.order_total = self.lineitems.aggregate(
            Sum('lineitem_total'))['lineitem_total__sum'] or 0
        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = (
                self.order_total * settings.STANDARD_DELIVERY_PERCENTAGE / 100
                )
        else:
            self.delivery_cost = 0
        self.grand_total = self.order_total + self.delivery_cost
        self.save()

    def save(self, *args, **kwargs):
        """
        Override the original save method. Set the order number if it hasn't
        been set already.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        """string method - return order number"""
        return self.order_number


class OrderLineItem(models.Model):
    """
    Individual shopping bag item
    After Order instance is created, iterate through the shopping bag, create
    order line item for each item, and attach these to the Order
    Doing this, update the three items above at the same time
    """
    order = models.ForeignKey(
        Order,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='lineitems'
        )
    product = models.ForeignKey(
        Product, null=False, blank=False, on_delete=models.CASCADE
        )
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=False,
        blank=False,
        editable=False
        )

    def save(self, *args, **kwargs):
        """
        Set total for each line item, override original save method
        to set this and update the order total
        """
        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        """string method - return sku plus order number"""
        return f'SKU {self.product.sku} on order {self.order.order_number}'
