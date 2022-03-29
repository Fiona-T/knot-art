"""Views for 'markets' app - craft markets seller will be attending"""
from django.shortcuts import render
import datetime
from .models import Market


def show_markets(request):
    """Show markets with date of today or later"""
    today = datetime.date.today()
    markets = Market.objects.filter(date__gte=today).order_by('date')
    context = {
        'markets': markets,
    }
    template = 'markets/markets.html'
    return render(request, template, context)
