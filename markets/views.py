"""Views for 'markets' app - craft markets seller will be attending"""
import datetime
from django.shortcuts import render
from .models import Market


def show_markets(request):
    """
    Show markets with date of today or later in date order
    If superuser, show all markets, newest first
    """
    today = datetime.date.today()
    if request.user.is_superuser:
        markets = Market.objects.all().order_by('-date')
    else:
        markets = Market.objects.filter(date__gte=today).order_by('date')
    context = {
        'markets': markets,
    }
    template = 'markets/markets.html'
    return render(request, template, context)
