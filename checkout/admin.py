"""admin set up for 'checkout' app, show OrderLineItem inside Orders"""
from django.contrib import admin
from .models import Order, OrderLineItem


class OrderLineItemAdminInline(admin.TabularInline):
    """
    OrderLineItems items will show up inside the relevant Order
    """
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


class OrderAdmin(admin.ModelAdmin):
    """
    Admin set up for Order model: List display, ordering, fields.
    """
    inlines = (OrderLineItemAdminInline,)
    readonly_fields = (
        'order_number', 'date', 'delivery_cost', 'order_total', 'grand_total',
        )
    fields = ('order_number', 'date', 'full_name',
              'email', 'phone_number', 'street_address1',
              'street_address2', 'town_or_city', 'county',
              'postcode', 'country', 'delivery_cost',
              'order_total', 'grand_total',)
    list_display = ('order_number', 'date', 'full_name',
                    'order_total', 'delivery_cost',
                    'grand_total',)
    ordering = ('-date',)


admin.site.register(Order, OrderAdmin)
