"""Views for 'markets' app - craft markets seller will be attending"""
from django.shortcuts import render
from .models import Market


def show_markets(request):
    """Show the markets"""
    markets = Market.objects.all()
    context = {
        'markets': markets,
    }
    template = 'markets/markets.html'
    return render(request, template, context)
