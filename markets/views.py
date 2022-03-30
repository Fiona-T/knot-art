"""Views for 'markets' app - craft markets seller will be attending"""
import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Market
from .forms import MarketForm


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


@login_required()
def add_market(request):
    """
    Show market form for admin user to add market. Raise 403 if not admin.
    """
    if not request.user.is_superuser:
        raise PermissionDenied()
    form = MarketForm()
    context = {
        'form': form,
    }
    template = 'markets/add_market.html'
    return render(request, template, context)
