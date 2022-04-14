"""Set up of django admin site for markets app"""
from django.contrib import admin
from .models import County, Market, Comment


@admin.register(County)
class CountyAdmin(admin.ModelAdmin):
    """
    County model - admin site set up:
    Show all fields in list display
    """
    list_display = ('friendly_name', 'name')


@admin.register(Market)
class MarketAdmin(admin.ModelAdmin):
    """
    Market model - admin set up: fields to show in list view,
    Allow filtering by county, and search by name + website.
    """
    list_display = (
        'name', 'location', 'county', 'date', 'website', 'date_passed',
        )
    list_filter = ('county',)
    search_fields = ['name', 'website', ]


admin.site.register(Comment)
