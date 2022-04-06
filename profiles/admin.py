"""Set up of django admin site for profiles app"""
from django.contrib import admin
from checkout.models import Order
from .models import UserProfile, SavedMarketList


class OrderAdminInline(admin.TabularInline):
    """
    Order instances to be shown inside the UserProfile.
    Fields are read only, with link to view/edit the full Order
    """
    model = Order
    show_change_link = True
    readonly_fields = (
        'order_number', 'date', 'full_name', 'email', 'grand_total'
        )
    fields = ['date', 'full_name', 'email', 'grand_total']


class SavedMarketListAdminInline(admin.TabularInline):
    """
    SavedMarketList to be shown inside the UserProfile.
    """
    model = SavedMarketList


class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin set up for UserProfile model - show the two inline models
    so user's Orders and SavedMarketList are accessible from this view
    """
    inlines = (OrderAdminInline, SavedMarketListAdminInline,)


admin.site.register(UserProfile, UserProfileAdmin)
