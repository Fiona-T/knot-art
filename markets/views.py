"""Views for 'markets' app - craft markets seller will be attending"""
import datetime
from django.shortcuts import render
from .models import Market


def show_markets(request):
    """
    Show markets with date of today or later, oldest date first
    If superuser, show all markets (default ordering, newest first)
    """
    today = datetime.date.today()
    if request.user.is_superuser:
        markets = Market.objects.all()
    else:
        markets = Market.objects.filter(date__gte=today).order_by('date')
    context = {
        'markets': markets,
    }
    template = 'markets/markets.html'
    return render(request, template, context)
