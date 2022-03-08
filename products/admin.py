"""Set up of django admin site for products app"""
from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Category model - admin site set up:
    Show all fields in list display
    """
    list_display = ('friendly_name', 'name')
