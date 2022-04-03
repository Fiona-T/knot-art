"""Views for 'markets' app - craft markets seller will be attending"""
import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_POST
from django.http import Http404
from django.contrib import messages
from profiles.models import SavedMarketList, UserProfile
from .models import Market
from .forms import MarketForm


def show_markets(request):
    """
    Show markets with date of today or later, oldest date first
    If superuser, show all markets (default ordering, newest first)
    If user logged in, get their saved markets list if they have one (so
    that template can show if market on their saved list or not)
    """
    today = datetime.date.today()
    if request.user.is_superuser:
        markets = Market.objects.all()
    else:
        markets = Market.objects.filter(date__gte=today).order_by('date')

    if request.user.is_authenticated:
        user_profile = get_object_or_404(UserProfile, user=request.user)
        try:
            saved_markets_list = get_object_or_404(
                SavedMarketList, user=user_profile
                )
        except Http404:
            saved_markets_list = None

    context = {
        'markets': markets,
        'saved_markets_list': saved_markets_list
    }
    template = 'markets/markets.html'
    return render(request, template, context)


@login_required()
def add_market(request):
    """
    Show market form for admin user to add market. Raise 403 if not admin.
    Handle posting of form, show success/error messages.
    """
    if not request.user.is_superuser:
        raise PermissionDenied()
    if request.method == 'POST':
        form = MarketForm(request.POST, request.FILES)
        if form.is_valid():
            market = form.save()
            messages.success(
                request, f'New market: "{market}" added!'
                )
            return redirect('markets')
        else:
            messages.error(
                request,
                'Market not added. Please check the form for errors and '
                're-submit.'
                )
    else:
        form = MarketForm()
    context = {
        'form': form,
    }
    template = 'markets/add_market.html'
    return render(request, template, context)


@login_required()
def edit_market(request, market_id):
    """
    Show form for admin user to edit existing market. Raise 403 if not admin.
    Handle posting of form, show success/error messages.
    """
    if not request.user.is_superuser:
        raise PermissionDenied()
    market = get_object_or_404(Market, pk=market_id)
    if request.method == 'POST':
        form = MarketForm(request.POST, request.FILES, instance=market)
        if form.is_valid():
            market = form.save()
            messages.success(
                request,
                f'Updates to market: "{market}" saved!'
                )
            return redirect('markets')
        else:
            messages.error(
                request,
                'Market NOT updated. Please check the form for errors and '
                're-submit.'
                )
    else:
        form = MarketForm(instance=market)
    context = {
        'market': market,
        'form': form,
    }
    template = 'markets/edit_market.html'
    return render(request, template, context)


@require_POST
@login_required
def delete_market(request, market_id):
    """
    View for admin user to delete market from front end.
    Raise 403 if not admin.
    Post request only: delete market, show success message.
    """
    if not request.user.is_superuser:
        raise PermissionDenied()
    market = get_object_or_404(Market, pk=market_id)
    market.delete()
    messages.success(
        request, f'Market: "{market}" deleted!'
        )
    return redirect('markets')
